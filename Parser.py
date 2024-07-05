import requests
import psycopg2
from sqlalchemy import engine as sql

jobname = "Программист C++"

conn = psycopg2.connect(dbname = "postgres", user = "postgres", password = "23491", host = "127.0.0.1")
cursor = conn.cursor()

def get_vac(num = 0, name = "", exp_id = "noExperience", emp_id = "full", sch_id = "fullDay"):
    param = {
        'text': name,
        'experience': exp_id,
        'employment': emp_id,
        'schedule': sch_id,
        'area': 1,
        'page': num,
        'per_page': 100,
        'responses_count_enabled': True,
    }

    req = requests.get('https://api.hh.ru/vacancies', param)

    if req.status_code == 200:
        data = req.json()
        req.close()

        vacancies = data.get("items", [])
        num_vacan = len(vacancies)
        
        if num_vacan > 0:
            for i, vacancy in enumerate(vacancies):

                vacancy_id = vacancy.get("id")
                vacancy_title = vacancy.get("name")
                vacancy_url = vacancy.get("alternate_url")
                vacancy_resp_count = vacancy.get("counters", {}).get("responses")
                vacancy_employment = vacancy.get("employment", {}).get("id")
                vacancy_experience = vacancy.get("experience", {}).get("id")
                vacancy_sched = vacancy.get("schedule", {}).get("id")

                try:
                    vacancy_startpay = vacancy.get("salary", {}).get('from')
                    vacancy_maxpay = vacancy.get("salary", {}).get('to')

                except:
                    vacancy_startpay = None
                    vacancy_maxpay = None
                
                """
                insert_cd = "INSERT INTO vacancies(id, name, start_sal, max_sal, vac_url, exp_type, emp_type, responses, sched_type) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                insert_value = (vacancy_id, vacancy_title, vacancy_startpay, vacancy_maxpay, vacancy_url, vacancy_experience, vacancy_employment, vacancy_resp_count, vacancy_sched)
                try:
                    cursor.execute(insert_cd, insert_value)
                except:
                    continue
                conn.commit()
                """

def mean_sal_vac():
    cursor.execute("SELECT AVG(start_sal)::numeric(10,0) FROM vacancies")
    for a in cursor:
        average = a[0]
    return average


#cursor.execute("DELETE FROM vacancies")
#cursor.close()
#conn.close()
#conn.commit() # сохр изменений



#mean_sal_vac()
#get_vac(0, jobname)