# src/server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict

from src.models.llm_analyze_freeform_input import analyze_freeform_input
from src.models.llm_followups import generate_followup_question
from src.models.llm_guidance import generate_guidance
from src.models.agent.concussion_agent import ConcussionAgent
from src.models.agent.rtp_qa import generate_rtp_response_rule_based, generate_rtp_response_llm
from src.utils.protocols.load_concussion_flow import load_concussion_flow
from src.utils.protocols.load_symptom_reference import load_symptom_reference

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ConcussionAgent()
symptom_reference = load_symptom_reference("data/protocols/symptoms_reference.yaml")
rtp_reference = load_concussion_flow("data/protocols/return_to_play.yaml")

@app.get("/ping")
def ping():
    return {"status": "ok"}

class AnalyzeRequest(BaseModel):
    free_text: str

@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    result = analyze_freeform_input(agent, req.free_text)
    return result

class FollowupRequest(BaseModel):
    final_responses: Dict
    question_list: List[Dict]

@app.post("/followups")
def followups(req: FollowupRequest):
    followup_qs = [generate_followup_question(q["id"], req.final_responses[q["id"]], q, req.final_responses) for q in req.question_list if q["id"] in req.final_responses]
    return {"followups": [q["followup_question"] for q in followup_qs]}

class GuidanceRequest(BaseModel):
    assessment_bundle: Dict

@app.post("/guidance")
def guidance(req: GuidanceRequest):
    return generate_guidance(req.assessment_bundle)

class RTPRequest(BaseModel):
    activity_name: str
    assessment_bundle: Dict

@app.post("/rtp")
def rtp(req: RTPRequest):
    return generate_rtp_response_rule_based(req.activity_name, req.assessment_bundle, rtp_reference)

class RTPAskRequest(BaseModel):
    question: str
    assessment_bundle: Dict

@app.post("/rtp/ask")
def rtp_ask(req: RTPAskRequest):
    return generate_rtp_response_llm(req.question, req.assessment_bundle, rtp_reference)
