import random
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import MNR

def index(request):
    start_inventory = None
    start_inventory_p = None

    if request.method == 'POST':
        # Retrieve form data
        gallons_delivered = int(request.POST.get('gallons_delivered', 0))
        regular = int(request.POST.get('regular', 0))
        super = int(request.POST.get('super', 0))
        premium = int(request.POST.get('premium', 0))
        gallons_delivered_p = int(request.POST.get('gallons_delivered_p', 0))

        # Calculate values
        gallons_pumped = regular + (super * 0.65)
        gallons_pumped_p = premium + (super * 0.35)

        if MNR.objects.count() == 0:
            # Calculate initial values
            start_inventory = int(request.POST.get('start_inventory', 0))
            start_inventory_p = int(request.POST.get('start_inventory_p', 0))
            book_inventory = start_inventory + gallons_delivered - gallons_pumped
            book_inventory_p = start_inventory_p + gallons_delivered_p - gallons_pumped_p
            estimated_gallons = book_inventory + random.randint(-5, 5)
            estimated_gallons_p = book_inventory_p + random.randint(-5, 5)
        else:
            latest_mnr = MNR.objects.latest('dayDay')
            start_inventory = latest_mnr.gallons
            start_inventory_p = latest_mnr.gallons_p
            book_inventory = start_inventory + gallons_delivered - gallons_pumped
            book_inventory_p = start_inventory_p + gallons_delivered_p - gallons_pumped_p
            estimated_gallons = book_inventory + random.randint(-10, 10)
            estimated_gallons_p = book_inventory_p + random.randint(-10, 10)

        daily = estimated_gallons - book_inventory
        dailyy = estimated_gallons_p - book_inventory_p

        try:
            latest_mnr = MNR.objects.latest('dayDay')
            day = latest_mnr.dayDay + 1
            number = latest_mnr.number + 1
        except MNR.DoesNotExist:
            day = 1
            number = 1

        initials = 'sj'

        mnr = MNR(
            id=number,  
            dayDay=day,
            start_inventory=start_inventory,
            gallons_delivered=gallons_delivered,
            gallons_pumped=gallons_pumped,
            book_inventory=book_inventory,
            gallons=estimated_gallons,
            daily=daily,
            initials=initials,
            number=number,
            regular=regular,
            super=super,
            premium=premium,
            start_inventory_p=start_inventory_p,
            gallons_delivered_p=gallons_delivered_p,
            gallons_pumped_p=gallons_pumped_p,
            book_inventory_p=book_inventory_p,
            gallons_p=estimated_gallons_p,
            Dailyy=dailyy,
            initials_p=initials,
        )
        mnr.save()

        return HttpResponseRedirect(reverse('results'))  # Redirect to the results page

    day = request.session.get('day', 1)

    return render(request, 'home/index.html', {'start_inventory': start_inventory, 'start_inventory_p': start_inventory_p, 'day': day})
def edit_day(request):
    if request.method == 'POST':
        day = int(request.POST.get('day', 1))

        # Store the updated day in session or database
        # Here, I'm assuming you have a user-specific session or database model to store the day value
        # Modify the code below to store the day value based on your implementation
        request.session['day'] = day

        return HttpResponseRedirect(reverse('index'))

    # Retrieve the current day from session or database and pass it to the template
    # Modify the code below to retrieve the day value based on your implementation
    day = request.session.get('day', 1)

    return render(request, 'home/edit_day.html', {'day': day})

from django.shortcuts import render
from .models import MNR
import random

def results(request):
    # Fetch data from the MySQL table using your model and order by day
    results = MNR.objects.order_by('dayDay')  # Use the correct field name for day from your model

    # Generate random decimal values for inches and inches_p fields
    for data in results:
        data.inches += random.random()
        data.inches_p += random.random()

    # Pass the data to the template
    context = {'results': results}
    return render(request, 'home/results.html', context)

import mysql.connector
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from .models import MNR


def leakcheck(request):
    # Establish a MySQL connection
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password=r"HIj8$2$29:$&>>]?]’so87€!]’",
        database="monthlyinventoryrecord"
    )

    # Create a cursor object
    cursor = conn.cursor()

    dayDay = datetime.strptime("2023-05-30", "%Y-%m-%d")
    previous_day = dayDay - timedelta(days=31)

    # Calculate the sum of Daily, Dailyy, Gallons Pumped, and Gallons PumpedP for the previous month
    cursor.execute(
        "SELECT SUM(Daily), SUM(Dailyy), SUM(`gallons_pumped`), SUM(`gallons_pumped_p`) FROM mnr WHERE dayDay >= %s AND dayDay < %s",
        (previous_day, dayDay)
    )

    sums = cursor.fetchone()

    sum_daily = sums[0] or 0
    sum_dailyy = sums[1] or 0
    sum_gallons_pumped = sums[2] or 0
    sum_gallons_pumped_p = sums[3] or 0

    sum_gallons_pumped_p = sums[3] or 0

    # Perform the leak check calculation and store the result
    if sum_gallons_pumped * 0.01 + 130 < sum_daily:
        leak_check_result_pumped = "NO"
    else:
        leak_check_result_pumped = "YES"

    if sum_gallons_pumped_p * 0.01 + 130 < sum_dailyy:
        leak_check_result_pumped_p = "NO"
    else:
        leak_check_result_pumped_p = "YES"

    leak_check_result = "NO" if leak_check_result_pumped == "NO" or leak_check_result_pumped_p == "NO" else "YES"

    # Close the MySQL connection
    cursor.close()
    conn.close()

    # Return the result as an HTTP response
    response = f"Leak Check For Regular: {leak_check_result}\nLeak Check For Premium: {leak_check_result_pumped_p}"
    return HttpResponse(response)

# Establish a MySQL connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password=r"HIj8$2$29:$&>>]?]’so87€!]’",
    database="monthlyinventoryrecord"
)

# Create a cursor object
cursor = conn.cursor()
def calculate_leak_check():
    dayDay = datetime.strptime("2023-06-30", "%Y-%m-%d")
    previous_day = dayDay - timedelta(days=31)

    # Calculate the sum of Daily, Dailyy, Gallons Pumped, and Gallons PumpedP for the previous month
    cursor.execute("SELECT SUM(Daily), SUM(Dailyy), SUM(`gallons_pumped`), SUM(`gallons_pumped_p`) FROM mnr WHERE dayDay >= %s AND dayDay < %s", (previous_day, dayDay))

    sums = cursor.fetchone()

    sum_daily = sums[0] or 0
    sum_dailyy = sums[1] or 0
    sum_gallons_pumped = sums[2] or 0
    sum_gallons_pumped_p = sums[3] or 0

    # Perform the leak check calculation and return the result
    if sum_gallons_pumped * 0.01 + 130 < sum_daily:
        leak_check_result_pumped = "NO"
    else:
        leak_check_result_pumped = "YES"

    if sum_gallons_pumped_p * 0.01 + 130 < sum_dailyy:
        leak_check_result_pumped_p = "NO"
    else:
        leak_check_result_pumped_p = "YES"

    leak_check_result = "NO" if leak_check_result_pumped == "NO" or leak_check_result_pumped_p == "NO" else "YES"

    return leak_check_result, leak_check_result_pumped_p
from django.shortcuts import redirect
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from .models import MNR
from django.shortcuts import render
import random

def generate_regular_pdf(request):
    # Retrieve MNR data for regular from the database
    mnr_data = MNR.objects.filter(regular__gt=0).order_by('dayDay')

    # Set up the PDF document with landscape orientation
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    # Create a table to display the MNR data for regular
    table_data = [['Day', 'Start Inv.', 'Gal.Del.', 'Gal. Pum.', 'BookInv.', 'Inches', 'Gallons', 'Daily', 'Init.']]
    total_gallons = 0  # Initialize total gallons
    total_daily = 0  # Initialize total daily

    leak_check_result, _ = calculate_leak_check()
    leak_check_text = f'Leak Check: {leak_check_result}'

    for mnr in mnr_data:
        inches = "{:.2f}".format(mnr.inches)
        gallons = str(mnr.gallons)
        daily = str(mnr.daily)
        total_gallons += float(gallons)  # Accumulate gallons for the sum
        total_daily += float(daily)  # Accumulate daily for the sum

        table_data.append([
            str(mnr.dayDay),
            str(mnr.start_inventory),
            str(mnr.gallons_delivered),
            str(mnr.gallons_pumped),
            str(mnr.book_inventory),
            inches,
            gallons,
            daily,
            str(mnr.initials),
        ])

    # Apply table styles
    table_style = TableStyle([
        # Table style configurations here
    ])

    # Calculate table width to fit the page
    table_width = landscape(letter)[0] - 2 * 40

    # Add the sum row
    sum_row = [
        '',
        '',
        '',
        '',
        '',
        '',
        f'Total Gallons: {total_gallons}',  # Display total gallons
        '',
        f'Total Daily: {total_daily}',  # Display total daily
        '',
    ]
    table_data.append(sum_row)

    # Create the table
    table = Table(table_data, style=table_style, colWidths=[table_width / len(table_data[0])] * len(table_data[0]))

    # Build the PDF content
    content = []
    content.append(Paragraph('Monthly Inventory Record - Regular', styles['Title']))
    content.append(table)
    content.append(Paragraph(leak_check_text, styles['Normal']))

    # Build the PDF document
    doc.build(content)

    # Set the buffer's position to the beginning
    buffer.seek(0)

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mnr_regular.pdf"'
    response.write(buffer.getvalue())

    return response


def generate_premium_pdf(request):
    # Retrieve MNR data for premium from the database
    mnr_data = MNR.objects.filter(premium__gt=0).order_by('dayDay')

    # Set up the PDF document with landscape orientation
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    styles = getSampleStyleSheet()

    # Create a table to display the MNR data for premium
    table_data = [['Day', 'Start Inv.', 'Gal.Del.', 'Gal. Pum.', 'BookInv.', 'Inches', 'Gallons', 'Daily', 'Init.']]
    total_gallons = 0  # Initialize total gallons
    total_daily = 0  # Initialize total daily

    leak_check_result, _ = calculate_leak_check()
    leak_check_text = f'Leak Check: {leak_check_result}'

    for mnr in mnr_data:
        inches = "{:.2f}".format(mnr.inches_p)
        gallons = str(mnr.gallons)
        daily = str(mnr.daily)
        total_gallons += float(gallons)  # Accumulate gallons for the sum
        total_daily += float(daily)  # Accumulate daily for the sum

        table_data.append([
            str(mnr.dayDay),
            str(mnr.start_inventory),
            str(mnr.gallons_delivered),
            str(mnr.gallons_pumped),
            str(mnr.book_inventory),
            inches,
            gallons,
            daily,
            str(mnr.initials),
        ])

    # Apply table styles
    table_style = TableStyle([
        # Table style configurations here
    ])

    # Calculate table width to fit the page
    table_width = landscape(letter)[0] - 2 * 40

    # Add the sum row
    sum_row = [
        '',
        '',
        '',
        '',
        '',
        '',
        f'Total Gallons: {total_gallons}',  # Display total gallons
        '',
        f'Total Daily: {total_daily}',  # Display total daily
        '',
    ]
    table_data.append(sum_row)

    # Create the table
    table = Table(table_data, style=table_style, colWidths=[table_width / len(table_data[0])] * len(table_data[0]))

    # Build the PDF content
    content = []
    content.append(Paragraph('Monthly Inventory Record - Premium', styles['Title']))
    content.append(table)
    content.append(Paragraph(leak_check_text, styles['Normal']))

    # Build the PDF document
    doc.build(content)

    # Set the buffer's position to the beginning
    buffer.seek(0)

    # Create a response object with PDF content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="mnr_premium.pdf"'
    response.write(buffer.getvalue())

    return response

from django.shortcuts import redirect
from jianco.models import MNR

def clear_data(request):
    # Clear all data from the database
    MNR.objects.all().delete()

    # Store the table HTML in the session
    request.session['table_html'] = get_table_html()

    # Set a flag in the session to indicate cleared data state
    request.session['cleared_data_state'] = True

    # Redirect to the "months" URL
    return redirect('months')

def get_table_html():
    # Fetch data from the MySQL table using your model and order by day
    results = MNR.objects.order_by('dayDay')  # Use the correct field name for day from your model

    # Generate the table HTML
    table_html = '<table>'  # Replace with your table structure
    for data in results:
        # Generate table rows for each data entry
        table_html += f'<tr><td>{data.dayDay}</td><td>{data.start_inventory}</td>...</tr>'  # Replace with your row structure
    table_html += '</table>'

    return table_html

from django.shortcuts import render
from .models import MNR

def months(request):
    # Fetch all data from the MNR model
    results = MNR.objects.all()

    # Pass the data to the template
    context = {'results': results}
    return render(request, 'home/months.html', context)
