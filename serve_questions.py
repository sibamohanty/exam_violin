from main import create_app,Questions,Answers
from  sqlalchemy.sql.expression import func, select
import psycopg2

app = create_app()

def return_radom_question_set(n):
    """ It goes through the question bank
    and selects n random Questions along with it's answer list
    it also randomizes the answer choice sequence
    """
    #select.order_by(func.random())
    questions= Questions.query.order_by(func.random()).first()
    #print (questions.question)
    #print (questions)
    questions_answers = Questions.query.order_by(func.random()).join(Answers).limit(3)
#    questions_answers = Questions.query.rder_by(func.random()).join(Answers).limit(10)

    for k in questions_answers :
        print (k.question)
    #print (questions_answers.column_descriptions)
    q_a= Questions.query.join(Answers)
    #print (q_a.column_descriptions)

#return_radom_question_set(10)

# Using psycopg2 directly as not ablt to get the string_aggr operator in sqlalchemy
def rand_questions(n):
    conn = psycopg2.connect(database="tutor", user="postgres", password="postgres",host= "localhost", port= 5432 )
    cur = conn.cursor()
    sql = "select question, string_agg(answer,'|') as choice,FIRST(answer_key) as answer_key" \
              ' from questions left join answers'\
              ' on (answers.question_id=questions.id) left join correct_answer'\
              ' on (questions.id= correct_answer.question_id)'\
              ' group by questions.id  limit 10;'

    cur.execute(sql)
    rows = cur.fetchall()
    for r in rows:
        print (r[0],r[])

#rand_questions(1)
