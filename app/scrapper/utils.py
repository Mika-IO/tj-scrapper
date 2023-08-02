import requests
from bs4 import BeautifulSoup
import re
import time
import uuid
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def is_valid_uuid(uuid_str: str) -> bool:
    try:
        uuid_obj = uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def validate_process_number(process_number: str) -> bool:
    process_number_regex = r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"
    is_valid = re.match(process_number_regex, process_number)
    return bool(is_valid)


def first_level_url(base_url: str, process_number: str) -> str:
    return f"{base_url}?processo.numero={process_number}"


def second_level_url(base_url: str, process_code: str) -> str:
    return f"{base_url}?processo.codigo={process_code}"


def has_second_level(base_url: str, process_number: str) -> tuple:
    url = (
        f"https://{base_url}cposg5/search.do?"
        + "conversationId="
        + "&paginaConsulta=0"
        + "&cbPesquisa=NUMPROC"
        + f"&numeroDigitoAnoUnificado={process_number[:15]}"
        + f"&foroNumeroUnificado={process_number[21:25]}"
        + f"&dePesquisaNuUnificado={process_number}"
        + "&dePesquisaNuUnificado=UNIFICADO"
        + "&dePesquisa="
        + "&tipoNuProcesso=UNIFICADO"
    )
    soup = get_soup(url)
    process_code = soup.find(id="processoSelecionado")
    if process_code:
        process_code = process_code.get("value")
        has = True
    else:
        process_code = ""
        has = False
    return has, process_code


def get_soup(url: str) -> BeautifulSoup:
    start = time.time()
    page = requests.get(url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    end = time.time()
    logger.info("INFO: execution_time: {:.6f} segundos".format(end - start))
    return soup


def get_text(url, soup: BeautifulSoup, tag_id: str) -> str:
    tag = soup.find(id=tag_id)
    if tag:
        return tag.text.strip().replace("  ", "")
    else:
        print(f"ERROR: error to get text {tag_id} in url: {url}")
        return ""


def get_parts(soup: BeautifulSoup, tag_id: str, lawyers=False) -> list:

    tag = soup.find(id=tag_id)
    trs = tag.find_all("tr", class_="fundoClaro")
    parts = []
    for tr in trs:
        part_tag = tr.find("span", class_="mensagemExibindo tipoDeParticipacao")
        part = part_tag.text.strip() if part_tag else None

        name_tag = tr.find("td", class_="nomeParteEAdvogado")
        name = name_tag.get_text(strip=True) if name_tag else None

        part = {
                "part": part,
                "name": name
            }
        if lawyers:
            lawyers = []
            lawyer_tags = name_tag.find_all("span", class_="mensagemExibindo")
            for lawyer_tag in lawyer_tags:
                if lawyer_tag.next_sibling:
                    lawyer = lawyer_tag.next_sibling.strip()
                    lawyers.append(lawyer)
                    name = name.replace(f"Advogado:{lawyer}", "")
                    name = name.replace(f"Advogada:{lawyer}", "")

            part["lawyers"] = lawyers
        parts.append(part)
        
    return parts


def get_moves(soup: BeautifulSoup, tag_id: str) -> list:
    tag = soup.find(id=tag_id)
    trs = tag.find_all("tr", class_="fundoClaro")
    moves = []
    for tr in trs:
        td_tags = tr.find_all("td")
        date_tag = td_tags[0]
        description_tag = td_tags[2]
        date = date_tag.text.strip().replace("  ", "")
        description = description_tag.text.replace("\n", " ").replace("\t", " ").strip()
        description = re.sub(r"\s+", " ", description)
        moves.append({"date": date, "description": description})
    return moves


def report(url: str, tj: str) -> dict:
    soup = get_soup(url)

    report = {}

    report["process_number"] = get_text(url, soup, "numeroProcesso")
    report["process_class"] = get_text(url, soup, "classeProcesso")
    report["process_area"] = get_text(url, soup, "areaProcesso")
    report["process_subject"] = get_text(url, soup, "assuntoProcesso")

    report["process_date"] = get_text(url, soup, "dataHoraDistribuicaoProcesso")[:10]

    match tj:
        case "ce":
            report["process_parts"] = get_parts(soup, "tablePartesPrincipais")
            # TODO encontrar juiz e valor na pagina de processo no TJCE
            # Ao que parece esses dados nao estao na pagina

        case "al":
            report["process_judge"] = get_text(url, soup, "juizProcesso")
            report["process_value"] = get_text(url, soup, "valorAcaoProcesso")
            report["process_parts"] = get_parts(soup, "tablePartesPrincipais", lawyers=True)

    report["process_moves"] = get_moves(soup, "tabelaTodasMovimentacoes")

    return report
