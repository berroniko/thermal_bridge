from src.berroutils.container.list_of_dict_container import ListOfDictContainer


class Psi(ListOfDictContainer):

    required_keys: set[str] = {'Bezeichnung', 'Psi-Wert'}
    alternative_keys: dict[str] = None

    # format: alternative_keys = {"alt_key": "unique_key"}

    def __str__(self):
        return 'psi'

    def _clean_data(self, data):
        return data