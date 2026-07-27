import json
import os

os.makedirs("data", exist_ok=True)

# 1. Constitution of India
const_records = []
if os.path.exists("processed/constitution.jsonl"):
    with open("processed/constitution.jsonl", "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                const_records.append(json.loads(line))

with open("data/constitution.json", "w", encoding="utf-8") as f:
    json.dump(const_records, f, indent=2, ensure_ascii=False)
print(f"Saved {len(const_records)} records to data/constitution.json")

# 2. Bharatiya Nyaya Sanhita (BNS, 2023)
bns_sections = [
    {
        "id": "BNS-1", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "1",
        "chapter": "Chapter I - Preliminary", "title": "Short title, commencement and application",
        "text": "(1) This Act may be called the Bharatiya Nyaya Sanhita, 2023. (2) It shall come into force on 1st July 2024.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-103", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "103",
        "chapter": "Chapter VI - Offences Affecting the Human Body", "title": "Punishment for murder (Replaces IPC Section 302)",
        "text": "(1) Whoever commits murder shall be punished with death or imprisonment for life, and shall also be liable to fine.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-115", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "115",
        "chapter": "Chapter VI - Offences Affecting the Human Body", "title": "Voluntarily causing hurt (Replaces IPC Section 323)",
        "text": "(1) Whoever does any act with intention of causing hurt to any person is punishable with imprisonment up to 1 year or fine up to Rs 10,000.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-199", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "199",
        "chapter": "Chapter XI - False Evidence and Offences Against Public Justice", "title": "Public servant disobeying direction under law (Refusal by police to record FIR)",
        "text": "Whoever, being a public servant, knowingly disobeys any direction of the law prohibiting him from requiring the attendance of any person, or fails to record any information given to him regarding cognizable offences (FIR), shall be punished with rigorous imprisonment for a term which shall not be less than six months but which may extend to two years, and shall also be liable to fine.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-246", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "246",
        "chapter": "Chapter XIV - Offences Against Public Justice", "title": "Giving or fabricating false evidence (Replaces IPC Section 193)",
        "text": "Whoever intentionally gives false evidence in any stage of a judicial proceeding, or fabricates false evidence for the purpose of being used in any stage of a judicial proceeding, shall be punished with imprisonment of either description for a term which may extend to seven years, and shall also be liable to fine.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-248", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "248",
        "chapter": "Chapter XIV - Offences Against Public Justice", "title": "False charge of offence made with intent to injure / Fake Allegations (Replaces IPC Section 211)",
        "text": "Whoever, with intent to cause injury to any person, institutes or causes to be instituted any criminal proceeding against that person, or falsely charges any person with having committed an offence, knowing that there is no just or lawful ground for such proceeding or charge against that person, shall be punished with imprisonment of either description for a term which may extend to seven years, or fine, or both.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-303", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "303",
        "chapter": "Chapter XVII - Offences Against Property", "title": "Theft (Replaces IPC Section 379)",
        "text": "(1) Whoever, intending to take dishonestly any movable property out of the possession of any person without consent, moves that property, commits theft.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-304", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "304",
        "chapter": "Chapter XVII - Offences Against Property", "title": "Snatching",
        "text": "(1) Theft is snatching if the offender forcibly seizes or grabs away movable property from any person. Imprisonment up to 3 years.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-316", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "316",
        "chapter": "Chapter XVII - Offences Against Property", "title": "Criminal breach of trust (Replaces IPC Section 406)",
        "text": "Whoever, being entrusted with property, dishonestly misappropriates or converts to his own use that property, commits criminal breach of trust.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-318", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "318",
        "chapter": "Chapter XVII - Offences Against Property", "title": "Cheating (Replaces IPC Section 420)",
        "text": "Whoever, by deceiving any person, fraudulently or dishonestly induces the person to deliver any property, commits cheating.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    },
    {
        "id": "BNS-351", "act": "Bharatiya Nyaya Sanhita, 2023", "act_short": "BNS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "351",
        "chapter": "Chapter XIX - Offences Relating to Criminal Intimidation", "title": "Criminal intimidation",
        "text": "Whoever threatens another with injury to his person, reputation or property with intent to cause alarm commits criminal intimidation.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20048"
    }
]

with open("data/bns.json", "w", encoding="utf-8") as f:
    json.dump(bns_sections, f, indent=2, ensure_ascii=False)
print(f"Saved {len(bns_sections)} records to data/bns.json")

# 3. Bharatiya Nagarik Suraksha Sanhita (BNSS, 2023)
bnss_sections = [
    {
        "id": "BNSS-35", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "35",
        "chapter": "Chapter V - Arrest of Persons", "title": "When police may arrest without warrant (Replaces CrPC Section 41)",
        "text": "(1) Any police officer may without a warrant arrest any person who commits a cognizable offence in presence of police officer or against whom credible information is received. (3) Notice of appearance shall be issued where arrest is not mandatory for offences under 7 years imprisonment.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-47", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "47",
        "chapter": "Chapter V - Arrest of Persons", "title": "Person arrested to be informed of grounds of arrest and right to bail (Replaces CrPC Section 50)",
        "text": "(1) Every police officer arresting any person without warrant shall forthwith communicate full particulars of the offence and grounds for arrest.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-58", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "58",
        "chapter": "Chapter V - Arrest of Persons", "title": "Person arrested not to be detained more than twenty-four hours (Replaces CrPC Section 57)",
        "text": "No police officer shall detain an arrested person in custody longer than 24 hours (excluding journey time) without a special order of a Magistrate.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-107", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "107",
        "chapter": "Chapter VII - Processes to Compel Production of Things", "title": "Power of police officer to seize property & mandatory receipt (Replaces CrPC Section 102)",
        "text": "(1) Any police officer may seize property alleged or suspected to be stolen. (2) The officer MUST report the seizure to the Magistrate and provide a formal seizure receipt/memo to the person.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-173", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "173",
        "chapter": "Chapter XII - Information to Police and Investigation Powers", "title": "Information in cognizable cases (Mandatory FIR Recording & Zero FIR) (Replaces CrPC Section 154)",
        "text": "(1) Every information relating to the commission of a cognizable offence given to an officer in charge of a police station SHALL be reduced to writing (FIR). Information may also be given electronically (Zero FIR / E-FIR).",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-175", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "175",
        "chapter": "Chapter XII - Information to Police and Investigation Powers", "title": "Remedy when Police Officer Refuses to Register FIR (Application to Magistrate) (Replaces CrPC Section 156(3))",
        "text": "(3) If the police officer refuses to register the FIR even after approaching the Superintendent of Police, any person aggrieved may file an application before the Judicial Magistrate having jurisdiction.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    },
    {
        "id": "BNSS-528", "act": "Bharatiya Nagarik Suraksha Sanhita, 2023", "act_short": "BNSS", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "528",
        "chapter": "Chapter XXXIX - Miscellaneous", "title": "Inherent powers of High Court to Quash False FIR / Malicious Charges (Replaces CrPC Section 482)",
        "text": "Nothing in this Sanhita shall be deemed to limit or affect the inherent powers of the High Court to make such orders as may be necessary to give effect to any order under this Sanhita, or to prevent abuse of the process of any Court or otherwise to secure the ends of justice (Quashing false FIRs & fake charges).",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20049"
    }
]

with open("data/bnss.json", "w", encoding="utf-8") as f:
    json.dump(bnss_sections, f, indent=2, ensure_ascii=False)
print(f"Saved {len(bnss_sections)} records to data/bnss.json")

# 4. Bharatiya Sakshya Adhiniyam (BSA, 2023)
bsa_sections = [
    {
        "id": "BSA-1", "act": "Bharatiya Sakshya Adhiniyam, 2023", "act_short": "BSA", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "1",
        "chapter": "Chapter I - Preliminary", "title": "Short title, application and commencement",
        "text": "Applies to all judicial proceedings in or before any Court.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20050"
    },
    {
        "id": "BSA-22", "act": "Bharatiya Sakshya Adhiniyam, 2023", "act_short": "BSA", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "22",
        "chapter": "Chapter II - Relevancy of Facts", "title": "Inadmissibility of confessions made to police officer",
        "text": "No confession made to a police officer shall be proved as against a person accused of any offence unless made in the immediate presence of a Magistrate.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20050"
    },
    {
        "id": "BSA-61", "act": "Bharatiya Sakshya Adhiniyam, 2023", "act_short": "BSA", "act_year": 2023, "jurisdiction": "Central", "unit_type": "section", "number": "61",
        "chapter": "Chapter V - Documentary Evidence", "title": "Admissibility of electronic or digital record",
        "text": "Electronic or digital records shall not be denied admissibility in evidence on the ground that it is an electronic or digital record.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/20050"
    }
]

with open("data/bsa.json", "w", encoding="utf-8") as f:
    json.dump(bsa_sections, f, indent=2, ensure_ascii=False)
print(f"Saved {len(bsa_sections)} records to data/bsa.json")

# 5. Specialized Acts
other_acts = [
    {
        "id": "MVA-207", "act": "Motor Vehicles Act, 1988", "act_short": "MVA", "act_year": 1988, "jurisdiction": "Central", "unit_type": "section", "number": "207",
        "chapter": "Chapter XIII - Offences, Penalties and Procedure", "title": "Power to detain vehicle without permit or registration",
        "text": "Any police officer or authorised officer may detain a motor vehicle. Seizure receipt must be provided to the owner/driver immediately.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/1798"
    },
    {
        "id": "NIA-138", "act": "Negotiable Instruments Act, 1881", "act_short": "NIA", "act_year": 1881, "jurisdiction": "Central", "unit_type": "section", "number": "138",
        "chapter": "Chapter XVII - Penalties in Case of Dishonour of Cheques", "title": "Dishonour of cheque for insufficiency of funds",
        "text": "Where a cheque drawn for discharge of debt is returned unpaid by bank, drawer is punishable with imprisonment up to 2 years or fine up to double the cheque amount.",
        "status": "in force", "source_url": "https://www.indiacode.nic.in/handle/123456789/2188"
    }
]

with open("data/other_acts.json", "w", encoding="utf-8") as f:
    json.dump(other_acts, f, indent=2, ensure_ascii=False)
print(f"Saved {len(other_acts)} records to data/other_acts.json")
