import stripe
import requests

STRIPE_SECRET_KEY="sk_test_eZwfHEY0eD5PkSrvQDCD9c7h00o7MfemSy"
STRIPE_PUBLISHABLE_KEY="pk_test_5oV6niANRFMtP6O5U1iE9NZt006SXCAcTi"
stripe.api_key = STRIPE_SECRET_KEY

charge=stripe.Charge.retrieve(
    "ch_1Gj2yuBrxQzNWUYzeKhkMDIo",
    api_key=STRIPE_SECRET_KEY
)

charge.save()
# print(charge)
expand=stripe.Charge.retrieve(
    "ch_1Gj2yuBrxQzNWUYzeKhkMDIo",
    expand=['customer']
)
# print(expand)

subscriptions=stripe.Charge.retrieve(
    'ch_1GoU6NBrxQzNWUYzztojG7y8',
    api_key=STRIPE_SECRET_KEY
)
#print(subscriptions)

subscriptions_expand=stripe.Charge.retrieve(
    'ch_1GoU6NBrxQzNWUYzztojG7y8',
    expand=['customer']
)

# print(subscriptions_expand['customer']['subscriptions'])
# print(subscriptions_expand['customer']['default_source'])
# print(subscriptions_expand['customer']['currency'])
# print(subscriptions_expand['customer']['invoice_prefix'])
# print(subscriptions_expand['customer']['sources']['data'][:1][0]['customer'])
# print(subscriptions_expand['customer']['sources']['data'][:1][0]['exp_year'])

# print(stripe.api_key)

stripe.Charge.create(
    amount=6000,
    currency="usd",
    description="My first test charge created for api docs",
    source="tok_amex",
    idempotency_key="QIe0Kq0BbnPoJzRp"
)

stripe.Charge.create(
    amount=3000,
    currency="usd",
    source="tok_amex",
    metadata={'order_id':'59844'},
    idempotency_key="QIe0zq0BbnPdJzRe"
)

customers=stripe.Customer.list(limit=3)
# print(customers)

# for customer in customers.auto_paging_iter():
#     # print(customers['data'][customer]['latest_invoice'])
#     print(customer)

customer=stripe.Customer.create()
print(customer.last_response.request_id)

# intent=stripe.PaymentIntent.retrieve(
#     "pi_1Gl9E0BrxQzNWUYzv3kSq8Sx",
#     stripe_version="2020-03-02"
# )
# intent.capture()

# r=requests.get('/v1/balance')
# print(r)
github_response=requests.get('https://api.github.com')
print(github_response.status_code)

if github_response.status_code==200:
    print('Success!!!')
elif github_response.status_code==404:
    print('Not Found!!!')

from requests.exceptions import HTTPError


for url in ['https://api.github.com','https://api.github.com/invalid/']:
    try:
        response=requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occured: {http_err}')
    except Exception as err:
        print(f'other error occured: {err}')
    else:
        print('Success!!!')

content=github_response.content
# print(content)
text=github_response.text
# print(text)
json=github_response.json()
# print(json)
headers=github_response.headers
# print(headers)
contentType=github_response.headers['Content-Type']
date=github_response.headers['date']
print(date)
response_queries=requests.get(
    'https://api.github.com/search/repositories',
    params={'q':'requests+language:python'}
)
print(response_queries)
json_response=response_queries.json()
repository=json_response['items'][0]
print(f'Repository name: {repository["name"]}')
print(f'Repository description: {repository["description"]}')

repos=requests.get(
    'https://api.github.com/search/repositories',
    params={'q':'requests+language:python'},
    headers={'Accept':'application/vnd.github.v3.text-match+json'}
)

json_repos=repos.json()
repository=json_repos['items'][0]
print(f'Text matches: {repository["text_matches"]}')

print(requests.post('https://httpbin.org/post',data={'key':'value'}))
post_response=requests.post('https://httpbin.org/post',json={'key':'value'})
get_json=post_response.json()
print(get_json['data'])
print(get_json['headers']['Content-Type'])
# print(get_json.headers['Content-Type'])
from getpass import getpass
data =requests.get('https://api.github.com/tutorialcreation',auth=('tutorialcreation','luther1996-'))
print(data)
