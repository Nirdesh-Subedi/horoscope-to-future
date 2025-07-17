from flask import Flask, render_template, request, jsonify
import datetime
import random
import json
import time
from math import sin, cos, radians

app = Flask(__name__)

# Load data files
with open('data/nepali_horoscope.json') as f:
    nepali_horoscope = json.load(f)
    
with open('data/planetary_data.json') as f:
    planetary_data = json.load(f)

class VedicAstrology:
    def __init__(self):
        self.rasi_names = [
            "Mesha", "Vrishabha", "Mithuna", "Karka", "Simha", "Kanya",
            "Tula", "Vrishchika", "Dhanu", "Makara", "Kumbha", "Meena"
        ]
        
        self.nakshatras = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", 
            "Ardra", "Punarvasu", "Pushya", "Ashlesha", "Magha", 
            "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", 
            "Swati", "Vishakha", "Anuradha", "Jyeshtha", "Mula", 
            "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", 
            "Shatabhisha", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
        ]
        
        self.planets = {
            "Sun": "Surya", "Moon": "Chandra", "Mars": "Mangal", 
            "Mercury": "Budha", "Jupiter": "Guru", "Venus": "Shukra",
            "Saturn": "Shani", "Rahu": "Rahu", "Ketu": "Ketu"
        }
    
    def calculate_lagna(self, birth_time, birth_place):
        # Simplified lagna calculation
        hour = int(birth_time.split(':')[0])
        return self.rasi_names[(hour // 2) % 12]
    
    def generate_kundali(self, birth_date, birth_time, birth_place):
        day = birth_date.day
        month = birth_date.month
        year = birth_date.year
        
        # Calculate planetary positions (simplified)
        positions = {}
        for planet in self.planets:
            positions[planet] = random.choice(self.rasi_names)
        
        # Calculate nakshatra
        nakshatra_index = (day + month + year) % 27
        nakshatra = self.nakshatras[nakshatra_index]
        
        # Calculate lagna
        lagna = self.calculate_lagna(birth_time, birth_place)
        
        return {
            "lagna": lagna,
            "nakshatra": nakshatra,
            "planetary_positions": positions,
            "tithi": self.get_tithi(birth_date),
            "yoga": self.get_yoga(birth_date),
            "karana": self.get_karana(birth_date)
        }
    
    def get_tithi(self, date):
        tithis = [
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima",
            "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
            "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
            "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Amavasya"
        ]
        return tithis[(date.day + date.month) % 30]
    
    def get_yoga(self, date):
        yogas = [
            "Vishkumbha", "Priti", "Ayushman", "Saubhagya", "Shobhana",
            "Atiganda", "Sukarma", "Dhriti", "Shoola", "Ganda",
            "Vriddhi", "Dhruva", "Vyaghata", "Harshana", "Vajra",
            "Siddhi", "Vyatipata", "Variyan", "Parigha", "Shiva",
            "Siddha", "Sadhya", "Shubha", "Shukla", "Brahma",
            "Indra", "Vaidhriti"
        ]
        return yogas[(date.day + date.month) % 27]
    
    def get_karana(self, date):
        karanas = [
            "Bava", "Balava", "Kaulava", "Taitila", "Gara",
            "Vanija", "Vishti", "Shakuni", "Chatushpada", "Naga",
            "Kimstughna"
        ]
        return karanas[(date.day + date.month) % 11]

class DreamInterpreter:
    def interpret(self, dream_text):
        keywords = {
            "water": "Emotions and subconscious mind",
            "falling": "Fear of losing control",
            "flying": "Desire for freedom",
            "teeth": "Anxiety about appearance or communication",
            "death": "Transformation or change",
            "money": "Values or self-worth",
            "snake": "Healing or hidden fears",
            "house": "Your sense of self",
            "chase": "Avoiding a problem",
            "wedding": "New union or commitment"
        }
        
        interpretations = []
        for word, meaning in keywords.items():
            if word in dream_text.lower():
                interpretations.append(meaning)
        
        if not interpretations:
            return "Your dream suggests hidden messages from your subconscious. Pay attention to recurring symbols."
        
        return "Your dream indicates: " + "; ".join(interpretations)

class CompatibilityAnalyzer:
    def analyze(self, person1, person2):
        signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
        
        p1_sign = person1['sign']
        p2_sign = person2['sign']
        
        p1_index = signs.index(p1_sign)
        p2_index = signs.index(p2_sign)
        
        distance = (p1_index - p2_index) % 12
        
        compatibility = {
            'love': random.randint(40, 95),
            'trust': random.randint(30, 90),
            'communication': random.randint(50, 100),
            'friendship': random.randint(60, 100),
            'marriage': random.randint(20, 85)
        }
        
        aspects = []
        if distance == 0:  # Same sign
            aspects.append("Great understanding but may lack balance")
        elif distance == 1 or distance == 11:  # Adjacent signs
            aspects.append("Challenging but can learn from each other")
        elif distance == 2 or distance == 10:  # Semi-sextile
            aspects.append("Needs effort but potential for growth")
        elif distance == 3 or distance == 9:  # Square
            aspects.append("Dynamic tension that can spark passion or conflict")
        elif distance == 4 or distance == 8:  # Trine
            aspects.append("Natural harmony and flow")
        elif distance == 5 or distance == 7:  # Sextile
            aspects.append("Easy cooperation and mutual benefit")
        elif distance == 6:  # Opposition
            aspects.append("Powerful attraction with polarizing differences")
        
        return {
            'compatibility': compatibility,
            'aspects': aspects,
            'pros': self.generate_pros(p1_sign, p2_sign),
            'cons': self.generate_cons(p1_sign, p2_sign),
            'secret_message': self.generate_secret_message(p1_sign, p2_sign)
        }
    
    def generate_pros(self, sign1, sign2):
        pros = {
            ("Aries", "Leo"): "Passionate and energetic partnership",
            ("Taurus", "Virgo"): "Practical and grounded connection",
            ("Gemini", "Libra"): "Intellectual and communicative bond",
            ("Cancer", "Scorpio"): "Deep emotional understanding",
            ("Sagittarius", "Aquarius"): "Adventurous and freedom-loving",
            ("Capricorn", "Taurus"): "Stable and secure relationship"
        }
        
        return pros.get((sign1, sign2), "Strong potential for mutual growth")
    
    def generate_cons(self, sign1, sign2):
        cons = {
            ("Aries", "Cancer"): "May struggle with emotional expression",
            ("Taurus", "Aquarius"): "Different approaches to change",
            ("Gemini", "Virgo"): "Communication styles may clash",
            ("Leo", "Scorpio"): "Power struggles possible",
            ("Libra", "Capricorn"): "Different social needs",
            ("Pisces", "Sagittarius"): "May have different reality perceptions"
        }
        
        return cons.get((sign1, sign2), "Need to work on understanding differences")
    
    def generate_secret_message(self, sign1, sign2):
        messages = [
            f"The stars whisper that {sign1} and {sign2} share a karmic connection",
            f"Cosmic alignment suggests {sign1} helps {sign2} grow in ways unseen",
            f"Hidden aspect reveals {sign2} holds the key to {sign1}'s heart",
            f"Ancient astrology texts speak of powerful bond between {sign1} and {sign2}"
        ]
        return random.choice(messages)

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/get_horoscope', methods=['POST'])
def get_horoscope():
    data = request.json
    birth_date = datetime.datetime.strptime(data['birth_date'], "%Y-%m-%d").date()
    birth_time = data['birth_time']
    birth_place = data['birth_place']
    language = data.get('language', 'english')
    
    # Generate predictions
    vedic = VedicAstrology()
    kundali = vedic.generate_kundali(birth_date, birth_time, birth_place)
    
    # Daily prediction
    daily_prediction = {
        'english': random.choice([
            "Today brings opportunities for personal growth.",
            "Unexpected news may arrive - stay open to change.",
            "Focus on health and wellbeing today.",
            "A chance encounter could be significant.",
            "Creative energy is strong - express yourself."
        ]),
        'nepali': random.choice(nepali_horoscope['daily'])
    }
    
    # Monthly prediction
    monthly_prediction = {
        'english': random.choice([
            "This month emphasizes relationships - nurture connections.",
            "Career matters take center stage - be proactive.",
            "Financial opportunities emerge but require careful consideration.",
            "Spiritual growth is highlighted - explore inner wisdom.",
            "Travel or education may bring important insights."
        ]),
        'nepali': random.choice(nepali_horoscope['monthly'])
    }
    
    # Lucky day calculation
    lucky_day = (birth_date.day + datetime.date.today().month) % 30 + 1
    if lucky_day > 30:
        lucky_day = 30
    
    response = {
        'kundali': kundali,
        'predictions': {
            'daily': daily_prediction,
            'monthly': monthly_prediction,
            'lucky_day': lucky_day
        },
        'sign': vedic.rasi_names[(birth_date.month + birth_date.day) % 12],
        'life_path': (birth_date.day + birth_date.month + birth_date.year) % 9 + 1
    }
    
    return jsonify(response)

@app.route('/interpret_dream', methods=['POST'])
def interpret_dream():
    dream_text = request.json.get('dream_text', '')
    interpreter = DreamInterpreter()
    interpretation = interpreter.interpret(dream_text)
    return jsonify({'interpretation': interpretation})

@app.route('/analyze_compatibility', methods=['POST'])
def analyze_compatibility():
    data = request.json
    analyzer = CompatibilityAnalyzer()
    result = analyzer.analyze(data['person1'], data['person2'])
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)