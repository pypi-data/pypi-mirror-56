from beancount.loader import load_file as beancount_load_file
from beancount.core.data import Transaction as beancount_Transaction

from webbean.modules.Account import Account
from webbean.core.Transaction import Transaction


class beancount(Account):

    account_type_name = 'beancount'
    resource_filename = 'beancount.jinja'

    def _get_all_transactions(self):

        res = beancount_load_file(self.filename)
        beancount_line = res[0]
        beancount_transactions = [line for line in beancount_line if isinstance(line, beancount_Transaction)]

        account_transactions = []
        for operation in beancount_transactions:
            for posting in operation.postings:
                if "Assets:CCP" in posting.account:
                    amount, _ = str(posting.units).split(" ")
                    transaction = Transaction(date=operation.date, amount=float(amount))
                    account_transactions.append(transaction)

        return account_transactions
