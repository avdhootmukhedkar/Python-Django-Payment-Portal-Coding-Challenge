import uuid
import razorpay

razorpay_details = {
    "key_id": 'rzp_test_here',
    "key_secret": 'secret_key_here'
}

order_id = uuid.uuid4()

client = razorpay.Client(auth = (razorpay_details["key_id"], razorpay_details["key_secret"]))
#order_amount  = 60000
#order_currency = 'INR'
#order_receipt = str(order_id)

#razorpay_order = client.order.create(dict(amount = order_amount, currency = order_currency, receipt = order_receipt))
#payment_id = 'pay_I5Knqr59QcSJ1I'
#payment_amount = 10000
#razorpay_refund = client.payment.refund(payment_id, payment_amount)


#print (razorpay_refund)
# DATA = {
#   "period": "weekly",
#   "interval": 1,
#   "item": {
#     "name": "Test plan - Weekly",
#     "amount": 69900,
#     "currency": "INR",
#     "description": "Description for the test plan - Weekly"
#   },
#   "notes": {
#     "notes_key_1": "Tea, Earl Grey, Hot",
#     "notes_key_2": "Tea, Earl Grey… decaf."
#   }
# }

# plan = client.plan.create(data=DATA)
# print (plan)

#print (razorpay_order)

# plans=client.plan.all()
# print (plans)

# subscriptions=client.subscription.all()
# print (subscriptions)
# # data = {
#   "plan_id":"plan_IEONjv3bZmtgIW",
#   "total_count":6,
  
# }
# subscribeToPlan=client.subscription.create(data=data)
# print(subscribeToPlan)
cancel=client.subscription.cancel("sub_ILT5nkWc6URtQz")
print(cancel)