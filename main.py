from flask import Flask, request, redirect, url_for,render_template
import sqlite3 as sql
from scipy.stats.stats import pearsonr 
from statsmodels.tsa.stattools import adfuller

app = Flask(__name__)



def get_units():
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM units')
    units = cursor.fetchall()
    conn.close()
    return units

def add_unit(year, unit, facilities, workforce, vehicles):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('INSERT INTO units (year, unit, facilities, workforce, vehicles) VALUES (?, ?, ?, ?, ?)',(year, unit, facilities, workforce, vehicles))
    conn.commit()
    conn.close()

def update_cost_unit(id, year, unit, facilities, workforce, vehicles):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('UPDATE units SET year = ?, unit= ?, facilities = ?, workforce = ?, vehicles =? WHERE id = ?',(year, unit, facilities, workforce, vehicles, id))
    conn.commit()
    conn.close()

def delete_unit(id):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('DELETE FROM units WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def get_unique_cost_units():
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT id, unit FROM units GROUP BY unit ORDER BY MIN(id) ASC;')
    unique_units = cursor.fetchall()
    conn.close()
    return unique_units

def get_unique_revenue_units():
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT id, unit FROM revenue_units GROUP BY unit ORDER BY MIN(id) ASC;')
    unique_units = cursor.fetchall()
    conn.close()
    return unique_units


def select_one_cost_unit(unit):

    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT year, unit, facilities, workforce, vehicles FROM units WHERE unit = ?', (unit,))
    unit = cursor.fetchall()
    conn.close()

    return unit

def select_one_revenue_unit(unit):

    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT year, unit, sales, ancillary FROM revenue_units WHERE unit = ?', (unit,))
    unit = cursor.fetchall()
    conn.close()

    return unit

def get_revenue_units():
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT * FROM revenue_units')
    revenue_units = cursor.fetchall()
    conn.close()
    return revenue_units

def add_revenue_unit(year, unit, sales, ancillary):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('INSERT INTO revenue_units (year, unit, sales, ancillary) VALUES (?, ?, ?, ?)',(year, unit, sales, ancillary))
    conn.commit()
    conn.close()

def update_revenue_unit(id, year, unit, sales, ancillary):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('UPDATE revenue_units SET year = ?, unit= ?, sales = ?, ancillary = ? WHERE id = ?',(year, unit, sales, ancillary, id))
    conn.commit()
    conn.close()

def delete_revenue_unit(id):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('DELETE FROM revenue_units WHERE id = ?', (id,))
    conn.commit()
    conn.close()


def check_unique_revenue_units(unit):
    conn=sql.connect('./database.db')
    cursor=conn.cursor()
    cursor.execute('SELECT id, unit FROM revenue_units WHERE unit = ? GROUP BY unit ORDER BY MIN(id) ASC;',(unit,))
    unique_units = cursor.fetchall()
    conn.close()
    return unique_units



@app.route('/')
def start_page(name=None):
    return render_template('start_page.html')

@app.route('/business_unit_cost_watch')
def business_unit_cost_watch(name=None):
    
    units = get_units()

    return render_template('business_unit_cost_watch.html', units=units)

@app.route('/add_unit', methods=['POST'])
def add_unit_route():
    year = request.form['year']
    unit = request.form['unit']
    facilities = request.form['facilities']
    workforce = request.form['workforce']
    vehicles = request.form['vehicles']
    add_unit(year, unit, facilities, workforce, vehicles)
    return redirect(url_for('business_unit_cost_watch'))

@app.route('/update_cost_unit/<int:id>', methods=['GET', 'POST'])
def update_cost_unit_route(id):
    if request.method == 'POST':
        year = request.form['year']
        unit = request.form['unit']
        facilities = request.form['facilities']
        workforce = request.form['workforce']
        vehicles = request.form['vehicles']
        update_cost_unit(id, year, unit, facilities, workforce, vehicles)
        return redirect(url_for('business_unit_cost_watch'))

    conn = sql.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM units WHERE id = ?',(id,))
    unit = cursor.fetchone()
    conn.close()
    return render_template('update_cost_unit.html', unit=unit)

@app.route('/delete_unit/<int:id>',methods=['GET'])
def delete_unit_route(id):
    delete_unit(id)
    return redirect(url_for('business_unit_cost_watch'))



@app.route('/business_unit_cost_visualisation')
def business_unit_cost_visualisation(name=None):

    units = get_unique_cost_units()
    array = []
    for element in units:
        array.append(element)

    return render_template('business_unit_cost_visualisation.html', array = array)


@app.route('/get_one_unit', methods=['GET', 'POST'])
def get_one_unit():

    #prepare for the dropdown
    units = get_unique_cost_units()
    array = []
    for element in units:
        array.append(element)
    
    #prepare data for graph
    unit = request.form.get('unit')
    unit = select_one_cost_unit(unit)

    labels = []
    for i in range(len(unit)):
        labels.append(unit[i][0])
    
    values = []
    for i in range(len(unit)):
        values.append((unit[i][2]+unit[i][3]+unit[i][4]))

    #prepare for the table , add in method in stackoverflow
    result = []
    for i in range(len(unit)):
        result.append((labels[i], values[i]))

    return render_template('business_unit_cost_visualisation.html', array = array, labels=labels, values=values, result=result)





@app.route('/business_unit_revenue_watch')
def business_unit_revenue_watch(name=None):
    
    units = get_revenue_units()

    return render_template('business_unit_revenue_watch.html', units=units)

@app.route('/add_revenue_unit', methods=['POST'])
def add_revenue_unit_route():
    year = request.form['year']
    unit = request.form['unit']
    sales = request.form['sales']
    ancillary = request.form['ancillary']
    add_revenue_unit(year, unit, sales, ancillary)
    return redirect(url_for('business_unit_revenue_watch'))

@app.route('/update_revenue_unit/<int:id>', methods=['GET', 'POST'])
def update_revenue_unit_route(id):
    if request.method == 'POST':
        year = request.form['year']
        unit = request.form['unit']
        sales = request.form['sales']
        ancillary = request.form['ancillary']
        update_revenue_unit(id, year, unit, sales,ancillary)
        return redirect(url_for('business_unit_revenue_watch'))

    conn = sql.connect('./database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM revenue_units WHERE id = ?',(id,))
    unit = cursor.fetchone()
    conn.close()
    return render_template('update_revenue_unit.html', unit=unit)

@app.route('/delete_revenue_unit/<int:id>',methods=['GET'])
def delete_revenue_unit_route(id):
    delete_revenue_unit(id)
    return redirect(url_for('business_unit_revenue_watch'))



@app.route('/business_unit_revenue_visualisation')
def business_unit_revenue_visualisation(name=None):

    units = get_unique_revenue_units()
    array = []
    for element in units:
        array.append(element)



    return render_template('business_unit_revenue_visualisation.html', array=array)


@app.route('/get_one_revenue_unit', methods=['GET', 'POST'])
def get_one_revenue_unit():

    units = get_unique_revenue_units()
    array = []
    for element in units:
        array.append(element)
    

    unit = request.form.get('unit')
    unit = select_one_revenue_unit(unit)

    #prepare for chart
    labels = []
    for i in range(len(unit)):
        labels.append(unit[i][0])
    
    values = []
    for i in range(len(unit)):
        values.append((unit[i][2] + unit[i][3]))

    #prepare for the table
    result = []
    for i in range(len(unit)):
        result.append((labels[i], values[i]))


    return render_template('business_unit_revenue_visualisation.html', array = array, labels=labels, values=values, result=result)


@app.route('/business_unit_cost_and_revenue_visualisation_with_revenue_alignment_indication')
def business_unit_cost_and_revenue_visualisation_with_revenue_alignment_indication(name=None):

    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #return revenue scheme and check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])


            
    return render_template('business_unit_cost_and_revenue_visualisation_with_revenue_alignment_indication.html', array = array)




@app.route('/get_one_cost_and_revenue_unit', methods=['GET', 'POST'])
def get_one_cost_and_revenue_unit(name=None):


    unit = request.form.get('unit')
    cost_unit = select_one_cost_unit(unit)
    revenue_unit = select_one_revenue_unit(unit)

    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])


    #prepare for chart  
    labels = []
    for i in range(len(cost_unit)):
        labels.append(cost_unit[i][0])
    
    cost_result = []
    for i in range(len(cost_unit)):
        cost_result.append((cost_unit[i][2] + cost_unit[i][3] + cost_unit[i][4]))

    revenue_result = []
    for i in range(len(revenue_unit)):
        revenue_result.append((revenue_unit[i][2] + revenue_unit[i][3]))


    #prepare for the table
    result = []
    for i in range(len(revenue_unit)):
        result.append((labels[i], cost_result[i], revenue_result[i]))

    #revenue alignment with pearson correlation
    revenue_alignment, pvalue = pearsonr(cost_result,revenue_result)

    revenue_alignment = round(revenue_alignment, 2)
                
    return render_template('business_unit_cost_and_revenue_visualisation_with_revenue_alignment_indication.html', array = array, labels=labels, cost_result=cost_result, revenue_result=revenue_result, result=result, revenue_alignment=revenue_alignment)



@app.route('/business_unit_gross_margin_visualisation_and_gross_profit')
def business_unit_gross_margin_visualisation_and_gross_profit(name=None):
        
    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #return revenue scheme and check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])


    return render_template('business_unit_gross_margin_visualisation_and_gross_profit.html', array=array)



@app.route('/get_one_cost_and_revenue_unit_for_gross_profit', methods=['GET', 'POST'])
def get_one_cost_and_revenue_unit_for_gross_profit(name=None):


    unit = request.form.get('unit')
    cost_unit = select_one_cost_unit(unit)
    revenue_unit = select_one_revenue_unit(unit)

    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])


    #prepare for chart  
    labels = []
    for i in range(len(cost_unit)):
        labels.append(cost_unit[i][0])
    
    cost_result = []
    for i in range(len(cost_unit)):
        cost_result.append((cost_unit[i][2] + cost_unit[i][3] + cost_unit[i][4]))

    revenue_result = []
    for i in range(len(revenue_unit)):
        revenue_result.append((revenue_unit[i][2] + revenue_unit[i][3]))

    gross_margin = []
    for i in range(len(revenue_unit)):
        gross_margin.append(-((cost_result[i]/revenue_result[i])-1))


    #prepare for the table
    gross_profit = []
    for i in range(len(revenue_unit)):
        gross_profit.append(revenue_result[i] * gross_margin[i])

    table_result = []
    for i in range(len(revenue_unit)):
        table_result.append((labels[i], round(gross_margin[i],2), int(round(gross_profit[i],0))))


                
    return render_template('business_unit_gross_margin_visualisation_and_gross_profit.html', array = array, labels=labels, gross_margin=gross_margin, table_result=table_result)




@app.route('/business_unit_markup_visualisation_and_markup_stability')
def business_unit_markup_visualisation_and_markup_stability(name=None):

    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #return revenue scheme and check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])

        
    return render_template('business_unit_markup_visualisation_and_markup_stability.html', array=array)


@app.route('/get_one_business_unit_markup_visualisation_and_markup_stability', methods=['GET', 'POST'])
def get_one_business_unit_markup_visualisation_and_markup_stability(name=None):


    unit = request.form.get('unit')
    cost_unit = select_one_cost_unit(unit)
    revenue_unit = select_one_revenue_unit(unit)

    cost_units = get_unique_cost_units()

    #check if revenue scheme is available
    check_list = []
    for i in range(len(cost_units)):
        if check_unique_revenue_units(str(cost_units[i][1])) != []:
            check_list.append((cost_units[i][1]))

    #check year alignment
    array = []
    for i in range(len(check_list)):

        one_cost_unit = select_one_cost_unit(str(check_list[i]))
        cost_years = []
        for j in range(len(one_cost_unit)):
            cost_years.append(one_cost_unit[j][0])

        one_revenue_unit = select_one_revenue_unit(str(check_list[i]))
        revenue_years = []
        for k in range(len(one_revenue_unit)):
            revenue_years.append(one_revenue_unit[k][0])

        if cost_years == revenue_years:
            array.append(check_list[i])


    #prepare for chart  
    labels = []
    for i in range(len(cost_unit)):
        labels.append(cost_unit[i][0])
    
    cost_result = []
    for i in range(len(cost_unit)):
        cost_result.append((cost_unit[i][2] + cost_unit[i][3] + cost_unit[i][4]))

    revenue_result = []
    for i in range(len(revenue_unit)):
        revenue_result.append((revenue_unit[i][2] + revenue_unit[i][3]))

    gross_margin = []
    for i in range(len(revenue_unit)):
        gross_margin.append(-((cost_result[i]/revenue_result[i])-1))

    gross_profit = []
    for i in range(len(revenue_unit)):
        gross_profit.append(revenue_result[i] * gross_margin[i])
    
    markup = []
    for i in range(len(revenue_unit)):
        markup.append(gross_profit[i] / cost_result[i])


    #prepare for the table
    table_result = []
    for i in range(len(revenue_unit)):
        table_result.append((labels[i], round(markup[i],2)))

    markup_stability = round(-1/adfuller(markup)[0], 2)

    return render_template('business_unit_markup_visualisation_and_markup_stability.html', array = array, labels=labels, markup=markup, table_result=table_result, markup_stability=markup_stability)



if __name__ == '__main__':
    app.run(debug=True)


