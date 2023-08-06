import os, time, metro2, json

class Metro2():

    def __init__(self, **kwargs):
        # Header segment section argument
        header_segment = kwargs.get('header_segment', {})
        self.efaxid = header_segment.get('efaxid', '')
        self.experianid = header_segment.get('experianid', '')
        self.adate = header_segment.get('adate', '')
        self.reporter_name = header_segment.get('reporter_name', '')
        self.reporter_address = header_segment.get('reporter_address', '')
        self.reporter_phone = header_segment.get('reporter_phone', '')

        # Base segment section argument
        base_segment = kwargs.get('base_segment', {})
        self.customer_account_number = base_segment.get('customer_account_number', '')
        self.time_stamp = base_segment.get('time_stamp', '')
        self.id_no = base_segment.get('id_no', '')
        self.portfolio_type = base_segment.get('portfolio_type', '')
        self.account_type = base_segment.get('account_type', '')
        self.date_opened = base_segment.get('date_opened', '')
        self.credit_limit = base_segment.get('credit_limit', '')
        self.hcla = base_segment.get('hcla', '')
        self.terms_duration = base_segment.get('terms_duration', '')
        self.terms_frequency = base_segment.get('terms_frequency', '')
        self.scheduled_monthly_payment_amount = base_segment.get('scheduled_monthly_payment_amount', '')
        self.actual_payment_amount = base_segment.get('actual_payment_amount', '')
        self.account_status = base_segment.get('account_status', '')
        self.payment_rating = base_segment.get('payment_rating', '')
        self.payment_history_profile = base_segment.get('scheduled_monthly_payment_amount', '')
        self.special_comment = base_segment.get('scheduled_monthly_payment_amount', '')
        self.compliance_condition_code = base_segment.get('scheduled_monthly_payment_amount', '')
        self.current_balance = base_segment.get('scheduled_monthly_payment_amount', '')
        self.amount_past_due = base_segment.get('scheduled_monthly_payment_amount', '')
        self.original_charge_off_amount = base_segment.get('scheduled_monthly_payment_amount', '')
        self.account_information_date = base_segment.get('account_information_date', '')
        self.first_delinquency_date = base_segment.get('first_delinquency_date', '')
        self.closed_date = base_segment.get('closed_date', '')
        self.last_payment_date = base_segment.get('last_payment_date', '')
        self.interest_type_indicator = base_segment.get('interest_type_indicator', '')
        self.consumer_transaction_type = base_segment.get('consumer_transaction_type', '')
        self.surname = base_segment.get('surname', '')
        self.first_name = base_segment.get('first_name', '')
        self.middle_name = base_segment.get('middle_name', '')
        self.generation_code = base_segment.get('generation_code', '')
        self.social_security_number = base_segment.get('social_security_number', '')
        self.date_of_birth = base_segment.get('date_of_birth', '')
        self.telephone_number = base_segment.get('telephone_number', '')
        self.ecoa_code = base_segment.get('ecoa_code', '')
        self.consumer_information_indicator = base_segment.get('consumer_information_indicator', '')
        self.country_code = base_segment.get('country_code', '')
        self.address_1 = base_segment.get('address_1', '')
        self.address_2 = base_segment.get('address_2', '')
        self.city = base_segment.get('city', '')
        self.state = base_segment.get('state', '')
        self.postal_code = base_segment.get('postal_code', '')
        self.address_indicator = base_segment.get('address_indicator', '')
        self.residence_code = base_segment.get('residence_code', '')

        # J1 & J2 segment section argument
        self.j1_segments = kwargs.get('j1_segments', [])
        self.j2_segments = kwargs.get('j2_segments', [])


    def get_metro2_report(self):
        metro2_filename = 'metro_2_' + str(int(round(time.time() * 1000)))
        path = os.path.dirname(os.path.abspath(metro2.__file__))
        # Header segment section argument
        ruby_command = 'ruby ' + path + '/ruby/index.rb --experianid ' + self.experianid + ' --efaxid ' + self.efaxid + \
        ' --adate ' + self.adate + ' --reporter_name ' + self.reporter_name + \
        ' --reporter_address ' + self.reporter_address + ' --reporter_phone ' + self.reporter_phone

        # Base segment section argument
        ruby_command += ' --time_stamp \"' + self.time_stamp + '\" --id_no ' + self.id_no + \
        ' --can ' + self.customer_account_number + ' --account_type ' + self.account_type + \
        ' --date_opened \"' + self.date_opened + '\" --credit_limit ' + self.credit_limit + \
        ' --hcla ' + self.hcla + ' --terms_duration ' + self.terms_duration + \
        ' --terms_frequency ' + self.terms_frequency + ' --smpy ' + self.scheduled_monthly_payment_amount + \
        ' --apa ' + self.actual_payment_amount + ' --account_status ' + self.account_status + \
        ' --payment_rating ' + self.payment_rating + ' --php ' + self.payment_history_profile + \
        ' --special_comment ' + self.special_comment + ' --ccc ' + self.compliance_condition_code + \
        ' --current_balance ' + self.current_balance + ' --apd ' + self.amount_past_due + \
        ' --ocoa ' + self.original_charge_off_amount + ' --aid ' + self.account_information_date + \
        ' --fdc ' + self.first_delinquency_date + ' --closed_date ' + self.closed_date + \
        ' --lpd ' + self.last_payment_date + ' --iti ' + self.interest_type_indicator + \
        ' --ctt ' + self.consumer_transaction_type + ' --surname ' + self.surname + \
        ' --first_name ' + self.first_name + ' --middle_name ' + self.middle_name + \
        ' --generation_code ' + self.generation_code + ' --ssn ' + self.social_security_number + \
        ' --dob ' + self.date_of_birth + ' --phone_no ' + self.telephone_number + \
        ' --ecoa_code ' + self.ecoa_code + ' --cii ' + self.consumer_information_indicator + \
        ' --country_code ' + self.country_code + ' --address_1 ' + self.address_1 + \
        ' --address_2 ' + self.address_2 + ' --city ' + self.city + \
        ' --state ' + self.state + ' --postal_code ' + self.postal_code + \
        ' --address_indicator ' + self.address_indicator + ' --residence_code ' + self.residence_code + \
        '--portfolio_type' + self.portfolio_type

        # J1 segment section argument
        ruby_command += " --j1_segments \'" + json.dumps(self.j1_segments)  + "\'"
        ruby_command += ' > ' + metro2_filename

        # J2 segment section argument
        ruby_command += " --j2_segments \'" + json.dumps(self.j2_segments)  + "\'"
        ruby_command += ' > ' + metro2_filename

        os.system(ruby_command)
        file_content = open(metro2_filename, 'r').read()
        os.remove(metro2_filename)
        return file_content

