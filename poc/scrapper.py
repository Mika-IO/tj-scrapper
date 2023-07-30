"""
    VALIDATE process number DONE
    FIRST level DONE
        GET entire page of the process DONE
        PARSE data from page DONE
    SECOND level
        Exist in second level 
            GET entire page of the process DONE
            PARSE data from page DONE

    TODO
    fix: DIFERENCES BETWHEEN TJCE AND TJAL
    process in parallel
"""

import requests
import re
import time
from bs4 import BeautifulSoup


def validate_process_number(process_number: str) -> bool:
    process_number_regex = r"^\d{7}-\d{2}\.\d{4}\.\d{1}\.\d{2}\.\d{4}$"
    is_valid = re.match(process_number_regex, process_number)
    return bool(is_valid)


def first_level_url(base_url, process_number: str) -> str:
    return f"{base_url}?processo.numero={process_number}"


def second_level_url(base_url, process_code: str) -> str:
    return f"{base_url}?processo.codigo={process_code}"


def has_second_level(base_url, process_number: str) -> tuple:
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
        print(url)
        has = False
    return has, process_code


def get_soup(url: str) -> BeautifulSoup:
    start = time.time()
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    end = time.time()
    print("execution_time: {:.6f} segundos".format(end - start))
    return soup


def get_text(url, soup: BeautifulSoup, tag_id: str) -> str:
    tag = soup.find(id=tag_id)
    if tag:
        return tag.text.strip().replace("  ", "")
    else:
        print(tag_id)
        return ""


def get_parts(soup: BeautifulSoup, tag_id: str) -> list:
    tag = soup.find(id=tag_id)
    trs = tag.find_all("tr", class_="fundoClaro")
    parts = []
    for tr in trs:
        part_tag = tr.find("span", class_="mensagemExibindo tipoDeParticipacao")
        part = part_tag.text.strip() if part_tag else None

        name_tag = tr.find("td", class_="nomeParteEAdvogado")
        name = name_tag.get_text(strip=True) if name_tag else None

        lawyers = []
        lawyer_tags = name_tag.find_all("span", class_="mensagemExibindo")
        for lawyer_tag in lawyer_tags:
            if lawyer_tag.next_sibling:
                lawyer = lawyer_tag.next_sibling.strip()
                lawyers.append(lawyer)
                name = name.replace(f"Advogado:{lawyer}", "")
                name = name.replace(f"Advogada:{lawyer}", "")

        parts.append(
            {
                "part": part,
                "name": name,
                "lawyers": lawyers,
            }
        )
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


def report(url: str) -> dict:
    soup = get_soup(url)

    report = {}

    report["process_number"] = get_text(url, soup, "numeroProcesso")
    report["process_class"] = get_text(url, soup, "classeProcesso")
    report["process_area"] = get_text(url, soup, "areaProcesso")
    report["process_subject"] = get_text(url, soup, "assuntoProcesso")
    report["process_date"] = get_text(url, soup, "dataHoraDistribuicaoProcesso")[:10]
    report["process_judge"] = get_text(url, soup, "juizProcesso")
    report["process_value"] = get_text(url, soup, "valorAcaoProcesso")

    report["process_parts"] = get_parts(soup, "tablePartesPrincipais")
    report["process_moves"] = get_moves(soup, "tabelaTodasMovimentacoes")

    return report
