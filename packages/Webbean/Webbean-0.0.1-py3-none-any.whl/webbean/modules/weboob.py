
from weboob.core import Weboob

from webbean.modules.Account import Account
from webbean.core.Transaction import Transaction


class weboob(Account):

    def _get_all_transactions(self):

        weboob = Weboob()
        backend = weboob.load_backends(names=['bp'])['bp']  # TODO Make it generic

        account_transactions = []
        for account in backend.iter_accounts():
            if account.label != 'COMPTE BANCAIRE':  # TODO Make it generic
                continue
            for weboob_transaction in backend.iter_history(account):
                transaction = Transaction(date=weboob_transaction.date,
                                          amount=float(weboob_transaction.amount),
                                          label=weboob_transaction.label)
                account_transactions.append(transaction)
        return account_transactions
