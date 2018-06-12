from flask import Flask, render_template, redirect, request, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
mysql = connectToMySQL('lead_gen_business')
app.secret_key="MySecret"
@app.route('/')
def index():
    all_clients = mysql.query_db("""select concat(clients.first_name," ",clients.last_name) as full_name, count(leads.registered_datetime) as leads
    from leads join sites on leads.site_id = sites.site_id
    join clients on clients.client_id = sites.client_id
    where leads.registered_datetime >= '2011/01/01' and leads.registered_datetime<'2012/01/01'
    group by clients.client_id;;""")
    print("Fetched all clients", all_clients)
    return render_template('lindex2.html', clients = all_clients)


if __name__ == "__main__":
    app.run(debug=True)