from flask import Flask, request
import gpt-2-simple.gpt_2_simple.gpt_2 as gpt2

session = gpt2.start_tf_sess()
gpt2.load_gpt2(session, run_name="discord")

def generate(question="",prompt="",temp=0.4):
  #gpt2.load_gpt2(session, run_name="SCP")
  generated = gpt2.generate(session, 
                              run_name="discord",
                              prefix=question+"\n"+prompt,
                              nsamples=5,
                              batch_size=5,
                              return_as_list=True,
                              top_k=40,
                              top_p=0.9,
                              temperature=temp,
                              length=30)[1]
  return generated
app = Flask(__name__)
@app.route('api/v3.6.3/nova1', methods=['POST'])
def chatbot_response():
  if not request.json or not 'question' in request.json or not 'context' in request.json:
    abort(400)
    
  context = request.json['context']
  question = request.json['question']
  generated = enerate(context+"Static: "+question,prompt="",temp=0.7).replace(context+"Static: "+question+"\n","").split("Static:")[0]
  result = {"answers": generated}
  return result, 201
@app.errorhandler(404)
def page_not_found(e):
  return {"error": "404, page not found"}, 404
if __name__ == '__main__':
  app.run(port=5000, debug=True)
