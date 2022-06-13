"""API Helper for fetching currencies."""
import requests
CONVERTER_URL = 'https://api.exchangerate-api.com/v4/latest/'


class CurrencyConverter:
	"""Convert currency"""

	available_currencies = [
		'INR', 'AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD',
		'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL',
		'BSD', 'BTN', 'BWP', 'BYN', 'BZD', 'CAD', 'CDF', 'CHF', 'CLP', 'CNY', 'COP', 'CRC',
		'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD',
		'FKP', 'FOK', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD',
		'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'IMP', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD',
		'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KID', 'KMF', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK',
		'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP',
		'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD', 'NGN', 'NIO', 'NOK', 'NPR',
		'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG', 'QAR', 'RON', 'RSD',
		'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS', 'SRD',
		'SSP', 'STN', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TVD',
		'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST', 'XAF',
		'XCD', 'XDR', 'XOF', 'XPF', 'YER', 'ZAR', 'ZMW', 'ZWL']

	rates = {}

	def __init__(self):
		"""Initialise with values."""

	def call_api(self, currency, target_currency):
		"""Call the api to get currency values."""
		response = requests.get(f"{CONVERTER_URL}{currency.upper()}")
		if response.status_code == 200:
			result = response.json()
			rates = result.get('rates')
			return rates.get(target_currency.upper(), 1)
		return 1

	def get_rate(self, currency, target_currency):
		"""Get rate."""
		key = f"{currency.upper()}-{target_currency.upper()}"
		if self.rates.get(key):
			return self.rates.get(key)
		else:
			rate = self.call_api(currency, target_currency)
			self.rates[key] = rate
			return rate

	def convert_amount(self, currency, target_currency, amount):
		"""Convert given amount to target currency"""
		rate = self.get_rate(currency, target_currency)
		try:
			amount = float(amount)
		except ValueError:
			amount = 0
		return amount * rate

	def generate_converted_csv(self, records, target_currency):
		"""Generate CSV with appended values."""
		parsed_row = []
		headers = records.fieldnames
		headers.extend(["Converted Currency", "Converted Amount"])
		for line in records:
			record = line.copy()
			currency = record.get('Currency')
			amount = record.get("Amount")
			converted_rate = "{:.2f}".format(self.convert_amount(currency, target_currency, amount))
			record.update({
				"Converted Currency": target_currency.upper(),
				"Converted Amount": converted_rate
			})
			parsed_row.append(record)
		return headers, parsed_row
