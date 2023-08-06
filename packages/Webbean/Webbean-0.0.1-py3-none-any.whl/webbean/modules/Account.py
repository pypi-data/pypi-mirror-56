import datetime

from jinja2 import Environment, PackageLoader


class Account:

    def __init__(self, filename):
        self.filename = filename

    def get_all_transactions(self, days_synced=None):
        date_limit = datetime.date.today() - datetime.timedelta(days=days_synced)
        trs = self._get_all_transactions()
        return [tr for tr in trs if tr.date > date_limit]

    def write_transactions(self, account_transactions):

        env = Environment(loader=PackageLoader('webbean',
                                               'resources/template'))
        template = env.get_template(self.resource_filename)

        account_transactions = sorted(account_transactions, key=lambda x: x.date)

        print(template.render(transactions=account_transactions))
