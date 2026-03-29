"""
MediAssistant 鈥?agents/planner.py
PlannerAgent: decides whether to use RAG retriever or direct LLM.
"""

from app.core.state import AgentState

# 鈹€鈹€ Medical Keywords 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€
MEDICAL_KEYWORDS = [
    # Symptoms
    "fever", "pain", "headache", "nausea", "vomiting", "diarrhea", "cough",
    "acne", "pimple", "skin", "rash", "itch", "cold", "flu",
    "shortness of breath", "chest pain", "abdominal pain", "back pain",
    "joint pain", "muscle pain", "fatigue", "weakness", "dizziness",
    "confusion", "memory loss", "seizure", "numbness", "tingling", "swelling",
    "bleeding", "bruising", "weight loss", "weight gain",
    "appetite loss", "sleep problems", "insomnia",
    # Conditions
    "cancer", "diabetes", "hypertension", "heart disease", "stroke", "asthma",
    "copd", "pneumonia", "bronchitis", "covid", "coronavirus",
    "infection", "virus", "bacteria", "fungal", "arthritis", "osteoporosis",
    "thyroid", "kidney disease", "liver disease", "hepatitis", "depression",
    "anxiety", "bipolar", "schizophrenia", "alzheimer", "parkinson", "epilepsy",
    # Medical terms
    "treatment", "therapy", "medication", "medicine", "prescription", "dosage",
    "side effects", "diagnosis", "prognosis", "surgery", "operation",
    "procedure", "test", "lab results", "blood test", "x-ray", "mri",
    "ct scan", "ultrasound", "biopsy", "screening", "prevention", "vaccine",
    "immunization", "rehabilitation", "recovery", "chronic", "acute",
    "syndrome", "disorder", "symptom", "cure", "remedy", "doctor", "hospital",
    # Body parts
    "heart", "lung", "kidney", "liver", "brain", "stomach", "intestine",
    "blood", "bone", "muscle", "nerve", "eye", "ear", "throat",
    "neck", "spine", "joint", "head", "chest", "abdomen", "leg", "arm",
]

MEDICAL_KEYWORDS_ZH = [
    "发烧", "疼痛", "头痛", "恶心", "呕吐", "腹泻", "咳嗽",
    "痤疮", "皮肤", "皮疹", "瘙痒", "感冒", "流感",
    "呼吸困难", "胸痛", "腹痛", "背痛", "关节痛", "肌肉痛",
    "乏力", "虚弱", "头晕", "意识混乱", "记忆减退", "抽搐",
    "麻木", "刺痛", "肿胀", "出血", "淤青", "体重下降", "体重增加",
    "食欲下降", "失眠", "睡眠问题",
    "癌症", "糖尿病", "高血压", "心脏病", "中风", "哮喘",
    "肺炎", "支气管炎", "新冠", "冠状病毒", "感染", "病毒", "细菌",
    "真菌", "关节炎", "骨质疏松", "甲状腺", "肾病", "肝病", "肝炎",
    "抑郁", "焦虑", "阿尔茨海默", "帕金森", "癫痫",
    "治疗", "疗法", "药物", "药", "处方", "剂量", "副作用",
    "诊断", "预后", "手术", "操作", "检查", "化验", "血检",
    "x光", "核磁", "ct", "超声", "活检", "筛查", "预防", "疫苗",
    "康复", "恢复", "慢性", "急性", "综合征", "疾病", "症状",
    "治愈", "缓解", "医生", "医院",
    "心脏", "肺", "肾", "肝", "大脑", "胃", "肠道", "血液",
    "骨", "肌肉", "神经", "眼", "耳", "喉咙", "颈部", "脊柱",
    "关节", "头", "胸", "腹部", "腿", "手臂",
]


def PlannerAgent(state: AgentState) -> AgentState:
    """Decide whether to use RAG retriever or direct LLM based on question content."""
    question = state["question"].lower()
    contains_medical = any(kw in question for kw in MEDICAL_KEYWORDS) or any(
        kw in question for kw in MEDICAL_KEYWORDS_ZH
    )
    state["current_tool"] = "retriever" if contains_medical else "llm_agent"
    state["retry_count"] = 0
    return state

