#!/usr/bin/ruby

# To parse options from command line
# See: https://ruby-doc.org/stdlib-2.6.5/libdoc/optparse/rdoc/OptionParser.html
# See example: https://docs.ruby-lang.org/en/2.1.0/OptionParser.html#class-OptionParser-label-Complete+example
require 'optparse'

# See: https://github.com/teamupstart/metro_2
# NOTE: This assume that metro_2 gem is installed on host machine as part of setup/deployment
# This can be installed via `gem install metro_2`
require 'metro_2'
require 'date'
require 'time'
options = {}
OptionParser.new do |opts|
  # Data for header segment

  opts.on("", "--efaxid [EFAXID]", "Equifax Program Identifier ") do |efaxid|
    options[:efaxid] = efaxid
  end
  opts.on("", "--experianid [EXPERIANID]", "Experian Program Identifier ") do |experianid|
    options[:experianid] = experianid
  end
  opts.on("", "--adate [adate]", "Activity Date ") do |adate|
    options[:adate] = adate
  end
  opts.on("", "--reporter_name [REPORTER_NAME]", "Reporter Name ") do |reporter_name|
    options[:reporter_name] = reporter_name
  end
  opts.on("", "--reporter_address [REPORTER_ADDRESS]", "Reporter Address ") do |reporter_address|
    options[:reporter_address] = reporter_address
  end
  opts.on("", "--reporter_phone [REPORTER_PHONE]", "Reporter Telephone Number ") do |reporter_phone|
    options[:reporter_phone] = reporter_phone
  end

  # Data for base segment
  opts.on("", "--time_stamp [TIME_STAMP]", "Time Stamp") do |time_stamp|
    options[:time_stamp] = time_stamp
  end
  opts.on("", "--id_no [ID_NUMBER]", "Identification Number") do |id_no|
    options[:id_no] = id_no
  end
  opts.on("", "--can [CUSTOMER_ACCOUNT_NUMBER]", "Customer account number for the loan") do |customer_account_number|
    options[:customer_account_number] = customer_account_number
  end
  opts.on("", "--portfolio_type [PORTFOLIO_TYPE]", "Portfolio Type") do |portfolio_type|
    options[:portfolio_type] = portfolio_type
  end
  opts.on("", "--account_type [ACCOUNT_TYPE]", "Account Type") do |account_type|
    options[:account_type] = account_type
  end
  opts.on("", "--date_opened [DATE_OPENED]", "Date Opened") do |date_opened|
    options[:date_opened] = date_opened
  end
  opts.on("", "--credit_limit [CREDIT_LIMIT]", "Credit Limit") do |credit_limit|
    options[:credit_limit] = credit_limit
  end
  opts.on("", "--hcla [HIGHEST_CREDIT]", "Highest Credit or Original Loan Amount ") do |hcla|
    options[:highest_credit_or_loan_amount] = hcla
  end
  opts.on("", "--terms_duration [TERM_DURATION]", "Terms Duration") do |terms_duration|
    options[:terms_duration] = terms_duration
  end
  opts.on("", "--terms_frequency [TERM_FREQUENCY]", "Terms Frequency") do |terms_frequency|
    options[:terms_frequency] = terms_frequency
  end
  opts.on("", "--smpy [SCHEDULED_PAYMENT]", "Scheduled Monthly Payment Amount") do |smpy|
    options[:scheduled_monthly_payment_amount] = smpy
  end
  opts.on("", "--apa [ACTUAL_AMOUNT]", "Actual Payment Amount") do |apa|
    options[:actual_payment_amount] = apa
  end
  opts.on("", "--account_status [ACCOUNT_STATUS]", "Account Status") do |account_status|
    options[:account_status] = account_status
  end
  opts.on("", "--payment_rating [PAYMENT_RATING]", "Payment Rating") do |payment_rating|
    options[:payment_rating] = payment_rating
  end
  opts.on("", "--php [PAYMENT_HISTORY_PROFILE]", "Payment History Profile") do |php|
      options[:payment_history_profile] = php
    end
  opts.on("", "--special_comment [SPECIAL_COMMENT]", "Special Comment") do |special_comment|
      options[:special_comment] = special_comment
    end
  opts.on("", "--ccc [CCC]", "Compliance Condition Code ") do |ccc|
    options[:compliance_condition_code] = ccc
  end
  opts.on("", "--current_balance [CURRENT_BALANCE]", "Current Balance") do |current_balance|
    options[:current_balance] = current_balance
  end
  opts.on("", "--apd [AMOUNT_PAST_DUE]", "Amount Past Due ") do |apd|
    options[:amount_past_due] = apd
  end
  opts.on("", "--ocoa [ORIGINAL_CHARGE_OFF_AMOUNT]", "Original Charge-off Amount ") do |ocoa|
    options[:original_charge_off_amount] = ocoa
  end
  opts.on("", "--aid [ACCOUT_INFORMATION_DATE]", "Date of Account Information ") do |aid|
    options[:account_information_date] = aid
  end
  opts.on("", "--fdc [FIRST_DELINQUENCY_DATE]", "FCRA Compliance/ Date of First Delinquency ") do |fdc|
    options[:first_delinquency_date] = fdc
  end
  opts.on("", "--closed_date [DATE_CLOSED]", "Date Closed") do |closed_date|
    options[:closed_date] = closed_date
  end
  opts.on("", "--lpd [DATE_OF_LAST_PAYMENT]", "Date of Last Payment") do |lpd|
    options[:last_payment_date] = lpd
  end
  opts.on("", "--iti [INTEREST_TYPE_INDICATOR]", "Interest Type Indicator") do |iti|
    options[:interest_type_indicator] = iti
  end
  opts.on("", "--ctt [CONSUMER_TRANSACTION_TYPE]", "Consumer Transaction Type") do |ctt|
    options[:consumer_transaction_type] = ctt
  end
  opts.on("", "--surname [SUR_NAME]", "Surname") do |surname|
    options[:surname] = surname
  end
  opts.on("", "--first_name [FIRST_NAME]", "First Name") do |first_name|
    options[:first_name] = first_name
  end
  opts.on("", "--middle_name [MIDDLE_NAME]", "Middle Name") do |middle_name|
    options[:middle_name] = middle_name
  end
  opts.on("", "--generation_code [GENERATION_CODE]", "Generation Code") do |generation_code|
    options[:generation_code] = generation_code
  end
  opts.on("", "--ssn [SSN]", "Social Security Number") do |ssn|
    options[:social_security_number] = ssn
  end
  opts.on("", "--dob [DOB]", "Date of Birth ") do |dob|
    options[:date_of_birth] = dob
  end
  opts.on("", "--phone_no [PHONE_NO]", "Telephone Number") do |phone_no|
    options[:telephone_number] = phone_no
  end
  opts.on("", "--ecoa_code [ECOA_CODE]", "ECOA Code") do |ecoa_code|
    options[:ecoa_code] = ecoa_code
  end
  opts.on("", "--cii [CII]", "Consumer Information Indicator") do |cii|
    options[:consumer_information_indicator] = cii
  end
  opts.on("", "--country_code [COUNTRY_CODE]", "Country Code") do |country_code|
    options[:country_code] = country_code
  end
  opts.on("", "--address_1 [ADDRESS_1]", "First Line of Address ") do |address_1|
    options[:address_1] = address_1
  end
  opts.on("", "--address_2 [ADDRESS_2]", "Second Line of Address") do |address_2|
    options[:address_2] = address_2
  end
  opts.on("", "--city [CITY]", "City") do |city|
    options[:city] = city
  end
  opts.on("", "--state [STATE]", "State") do |state|
    options[:state] = state
  end
  opts.on("", "--postal_code [POSTAL_CODE]", "Postal/Zip Code") do |postal_code|
    options[:postal_code] = postal_code
  end
  opts.on("", "--address_indicator [ADDRESS_INDICATOR]", "Address Indicator ") do |address_indicator|
    options[:address_indicator] = address_indicator
  end
  opts.on("", "--residence_code [RESIDENCE_CODE]", "Residence Code") do |residence_code|
    options[:residence_code] = residence_code
  end

  opts.on("", "--j2_segments [J2_SEGMENTS]", "J2 Segment") do |j2_segments|
    j2_segments = j2_segments.gsub('[', '').gsub(']', '').split('}, {')
    j2_segments_hash = []
    j2_segments.each do |j2_segment|
      j2_segment = j2_segment.gsub('{', '').gsub('}', '').split(',')
      j2_segment_hash = {}
      j2_segment.each do |e|
        key_value = e.split(':')
        j2_segment_hash[key_value[0].gsub(' ', '').gsub('"', '')] = key_value[1].delete(" ").gsub('"', '')
      end
      j2_segments_hash.push(j2_segment_hash)
    end

    options[:j2_segments] = j2_segments_hash
  end

  opts.on("", "--j1_segments [J1_SEGMENTS]", "J1 Segment") do |j1_segments|
    j1_segments = j1_segments.gsub('[', '').gsub(']', '').split('}, {')
    j1_segments_hash = []
    j1_segments.each do |j1_segment|
      j1_segment = j1_segment.gsub('{', '').gsub('}', '').split(',')
      j1_segment_hash = {}
      j1_segment.each do |e|
        key_value = e.split(':')
        j1_segment_hash[key_value[0].gsub(' ', '').gsub('"', '')] = key_value[1].delete(" ").gsub('"', '')
      end
      j1_segments_hash.push(j1_segment_hash)
    end

    options[:j1_segments] = j1_segments_hash
  end

end.parse!

# Header segment attributes
metro_2_content = Metro2::Metro2File.new
metro_2_content.header.cycle_number = Time.new.day.to_s
metro_2_content.header.equifax_program_identifier = options[:efaxid]
metro_2_content.header.experian_program_identifier = options[:experianid]
metro_2_content.header.activity_date = Time.parse(options[:adate])
metro_2_content.header.created_date = Time.new
metro_2_content.header.reporter_name = options[:reporter_name]
metro_2_content.header.reporter_address = options[:reporter_address]
metro_2_content.header.reporter_telephone_number = options[:reporter_phone]

# Base segment attributes
base_segment = Metro2::Records::BaseSegment.new
base_segment.time_stamp = Time.parse(options[:time_stamp]) if options[:time_stamp]
# base_segment.correction_indicator = 0
base_segment.identification_number = options[:id_no]
base_segment.cycle_number = Time.new.day.to_s
base_segment.consumer_account_number = options[:consumer_account_number]
base_segment.portfolio_type = options[:portfolio_type]
base_segment.account_type = options[:account_type]
base_segment.date_opened = Time.parse(options[:date_opened]) if options[:date_opened]
base_segment.credit_limit = options[:credit_limit]
base_segment.highest_credit_or_loan_amount = options[:highest_credit_or_loan_amount]
base_segment.terms_duration = options[:terms_duration]
base_segment.terms_frequency = options[:terms_frequency]
base_segment.scheduled_monthly_payment_amount = options[:scheduled_monthly_payment_amount]
base_segment.actual_payment_amount = options[:actual_payment_amount]
base_segment.account_status = options[:account_status]
base_segment.payment_rating = options[:payment_rating]
base_segment.payment_history_profile = options[:payment_history_profile]
base_segment.special_comment = options[:special_comment]
base_segment.compliance_condition_code = options[:compliance_condition_code]
base_segment.current_balance = options[:current_balance]
base_segment.amount_past_due = options[:amount_past_due]
base_segment.original_charge_off_amount = options[:original_charge_off_amount]
base_segment.account_information_date = Time.parse(options[:account_information_date]) if options[:account_information_date]
base_segment.first_delinquency_date = Time.parse(options[:first_delinquency_date]) if options[:first_delinquency_date]
base_segment.closed_date = Time.parse(options[:closed_date]) if options[:closed_date]
base_segment.last_payment_date = Time.parse(options[:last_payment_date]) if options[:last_payment_date]
base_segment.interest_type_indicator = options[:interest_type_indicator]
base_segment.consumer_transaction_type = options[:consumer_transaction_type]
base_segment.surname = options[:surname]
base_segment.first_name = options[:first_name]
base_segment.middle_name = options[:middle_name]
base_segment.generation_code = options[:generation_code]
base_segment.social_security_number = options[:social_security_number]
base_segment.date_of_birth = Time.parse(options[:date_of_birth]) if options[:date_of_birth]
base_segment.telephone_number = options[:phone_no]
base_segment.ecoa_code = options[:ecoa_code]
base_segment.consumer_information_indicator = options[:consumer_information_indicator]
base_segment.country_code = options[:country_code]
base_segment.address_1 = options[:address_1]
base_segment.address_2 = options[:address_2]
base_segment.city = options[:city]
base_segment.state = options[:state]
base_segment.postal_code = options[:postal_code]
base_segment.address_indicator = options[:address_indicator]
base_segment.residence_code = options[:residence_code]

if options[:j1_segments]
  options[:j1_segments].each do |el|
    j1_segment = Metro2::Records::J1Segment.new
    j1_segment.surname = el['surname']
    j1_segment.first_name = el['first_name']
    j1_segment.generation_code = el['generation_code']
    j1_segment.social_security_number = el['social_security_number']
    j1_segment.date_of_birth = Time.parse(el['date_of_birth'])
    j1_segment.telephone_number = el['telephone_number']
    j1_segment.ecoa_code = el['ecoa_code']
    j1_segment.consumer_information_indicator = el['consumer_information_indicator']
    base_segment.j1_segment = [j1_segment]
  end
end

if options[:j2_segments]
  options[:j2_segments].each do |el|
    j2_segment = Metro2::Records::J2Segment.new
    j2_segment.surname = el['surname']
    j2_segment.first_name = el['first_name']
    j2_segment.generation_code = el['generation_code']
    j2_segment.social_security_number = el['social_security_number']
    j2_segment.date_of_birth = Time.parse(el['date_of_birth'])
    j2_segment.telephone_number = el['telephone_number']
    j2_segment.ecoa_code = el['ecoa_code']
    j2_segment.consumer_information_indicator = el['consumer_information_indicator']
    j2_segment.country_code = el['country_code']
    j2_segment.address_1 = el['address_1']
    j2_segment.address_2 = el['address_2']
    j2_segment.city = el['city']
    j2_segment.state = el['state']
    j2_segment.postal_code = el['postal_code']
    j2_segment.address_indicator = el['address_indicator']
    j2_segment.residence_code = el['residence_code']
    base_segment.j2_segment = [j2_segment]
  end
end

metro_2_content.base_segments << base_segment

puts metro_2_content.to_s # contents to write to file