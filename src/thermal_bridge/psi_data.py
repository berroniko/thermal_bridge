import re

from berroutils.container.list_of_dict_container import ListOfDictContainer

from src.utils import is_nan, parse_date


class Psi(ListOfDictContainer):
    required_keys: set[str] = {'Waermebruecke', 'Bezeichnung', 'Psi-Wert', 'Datum', 'row_color'}
    alternative_keys: dict[str] = {'Wärmebrücke'                     : 'Waermebruecke',
                                   'Zusatzinfo W\u00e4rmebr\u00fccke': 'Zusatzinfo Waermebruecke', }

    # format: alternative_keys = {"alt_key": "unique_key"}

    def __str__(self):
        return 'psi'

    def _clean_data(self, data):
        cleaned = []
        for elem in data:
            if is_nan(elem.get('Bezeichnung')) or is_nan(elem.get('Psi-Wert')):
                continue

            new_elem = {k: "-" if is_nan(v) else v for k, v in elem.items()}
            # new_elem["VHAG"] = 'X' if (elem.get('VHAG') in ['x', 'X']) else '-'

            del new_elem["BV"]
            del new_elem["Name"]
            for colum_name in elem.keys():
                if colum_name.startswith('Unnamed'):
                    del new_elem[colum_name]

            new_elem = new_elem | self._parse_bezeichnung(elem.get("Bezeichnung", ""))
            if False:  # handling of date formats
                datum = elem.get('Datum')
                if is_nan(datum):
                    new_elem['Datum'] = None
                else:
                    new_elem['Datum'] = parse_date(elem.get('Datum')).strftime("%Y-%m-%d")
            cleaned.append(new_elem)
        return cleaned

    @staticmethod
    def _parse_bezeichnung(bezeichnung: str) -> dict:
        result = {
            'staerke' : '-',
            'material': '-',
            'PPW'     : '-',
            'dicke'   : None,
            'WLG'     : None
        }

        # Match staerke (e.g., AW44, AWEG44)
        match_staerke = re.search(r'^([A-Z]+\d{2})', bezeichnung)
        if match_staerke:
            result['staerke'] = match_staerke.group()

        # Match material (e.g. -P-, -V-)
        match_material = re.search(r'-([A-Z])-', bezeichnung)
        if match_material:
            result['material'] = match_material.group(1)

        # Match PPW (e.g., PPW2, PPW4)
        match_PPW = re.search(r'(PPW\d)', bezeichnung)
        if match_PPW:
            result['PPW'] = match_PPW.group(1)

        # Match all thickness and WLG pairs like 160mm032
        thickness_match = re.search(r'(\d{2,4})mm(\d{3})', bezeichnung)
        if thickness_match:
            # Take the first one as per test expectation
            result['dicke'] = int(thickness_match.group(1))
            result['WLG'] = thickness_match.group(2)

        return result
