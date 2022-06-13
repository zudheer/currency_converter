import codecs
import csv

from django import forms
from django.http import HttpResponse

from converter.api_util import CurrencyConverter
from converter.excel_utils import generate_sub_category_excel


class CSVUploadForm(forms.Form):
	csv_file = forms.FileField(widget=forms.FileInput(attrs={'accept': ".csv"}))
	currency = forms.ChoiceField(choices=[(currency, currency) for currency in CurrencyConverter.available_currencies])
	export = forms.ChoiceField(choices=[('csv', 'CSV'), ('excel', 'EXCEL')])

	def __init__(self, *args, **kwargs):
		"""Documentation for ."""
		super().__init__(*args, **kwargs)
		for visible in self.visible_fields():
			visible.field.widget.attrs['class'] = 'form-control'
			visible.field.required = True

	def parse_csv(self):
		csv_file = self.cleaned_data['csv_file']
		converter_helper = CurrencyConverter()
		target_currency = self.cleaned_data['currency']
		export_type = self.cleaned_data['export']
		try:
			csv.Sniffer().sniff(csv_file.read(102400).decode('UTF-8'))
			csv_file.seek(0)
		except Exception as e:
			raise forms.ValidationError("Upload a valid CSV file!")
		try:
			records = csv.DictReader(codecs.iterdecode(self.cleaned_data['csv_file'], 'utf-8'))
		except Exception as e:
			raise forms.ValidationError(e.message)
		headers, converted_data = converter_helper.generate_converted_csv(records, target_currency=target_currency)
		if export_type == 'csv':
			return self.get_generated_csv(headers, converted_data)
		else:
			return self.get_generated_excel(headers, converted_data)

	@staticmethod
	def get_generated_csv(headers, converted_data):
		"""Generate and send parsed CSV."""

		response = HttpResponse(content_type='text/csv')
		response['Content-Disposition'] = 'attachment; filename="converted_rates.csv"'

		writer = csv.DictWriter(response, dialect='excel', fieldnames=headers)
		writer.writeheader()
		writer.writerows(converted_data)
		return response

	@staticmethod
	def get_generated_excel(headers, converted_data):
		"""Generate and send parsed Excel."""
		generated_excel = generate_sub_category_excel(headers, converted_data)
		filename = '{0}.xlsx'.format("converted_rates")
		response = HttpResponse(
			generated_excel,
			content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
		)
		response['Content-Disposition'] = 'attachment; filename=%s' % filename
		return response

