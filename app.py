# Import Dataset dari data_fetcher
from data_fetcher import DataFetcher

# Class utama MBTI
class BayesianMBTIApp:
    def __init__(self):
        # Probabilitas 16 tipe
        self.mbti_types = [
            "ISTJ",  # Introverted, Sensing, Thinking, Judging
            "ISFJ",  # Introverted, Sensing, Feeling, Judging
            "INFJ",  # Introverted, Intuitive, Feeling, Judging
            "INTJ",  # Introverted, Intuitive, Thinking, Judging
            "ISTP",  # Introverted, Sensing, Thinking, Perceiving
            "ISFP",  # Introverted, Sensing, Feeling, Perceiving
            "INFP",  # Introverted, Intuitive, Feeling, Perceiving
            "INTP",  # Introverted, Intuitive, Thinking, Perceiving
            "ESTP",  # Extraverted, Sensing, Thinking, Perceiving
            "ESFP",  # Extraverted, Sensing, Feeling, Perceiving
            "ENFP",  # Extraverted, Intuitive, Feeling, Perceiving
            "ENTP",  # Extraverted, Intuitive, Thinking, Perceiving
            "ESTJ",  # Extraverted, Sensing, Thinking, Judging
            "ESFJ",  # Extraverted, Sensing, Feeling, Judging
            "ENFJ",  # Extraverted, Intuitive, Feeling, Judging
            "ENTJ",  # Extraverted, Intuitive, Thinking, Judging
        ]
        
        # Deskripsi singkat tiap tipe MBTI
        self.mbti_descriptions = {
            "ISTJ": "ISTJ (The Inspector): Cocok menjadi Data Analyst, IT Auditor, atau Administrator Sistem karena teliti, bertanggung jawab, dan menghargai struktur.",
            "ISFJ": "ISFJ (The Protector): Bisa bekerja sebagai Quality Assurance (QA), Technical Support, atau IT Trainer berkat sifat penuh perhatian dan suka membantu.",
            "INFJ": "INFJ (The Advocate): Sangat cocok untuk menjadi UX Designer, Project Manager, atau Konsultan IT karena visioner dan idealis.",
            "INTJ": "INTJ (The Mastermind): Berpotensi menjadi Software Architect, AI Specialist, atau Cybersecurity Analyst dengan kemampuan strategis dan logis.",
            "ISTP": "ISTP (The Crafter): Cocok dalam peran seperti Network Engineer, IoT Developer, atau Teknisi Hardware dengan ketenangan dan keahlian teknis.",
            "ISFP": "ISFP (The Artist): Cocok sebagai Game Developer, UI Designer, atau Multimedia Specialist dengan sensitivitas dan kreativitas artistik.",
            "INFP": "INFP (The Mediator): Ideal untuk menjadi Content Strategist, Data Scientist, atau Software Developer yang dipandu nilai pribadi.",
            "INTP": "INTP (The Thinker): Cocok sebagai Peneliti AI, Programmer, atau Data Engineer dengan kemampuan analitis dan logis.",
            "ESTP": "ESTP (The Dynamo): Cocok menjadi IT Consultant, Entrepreneur Teknologi, atau Product Manager berkat energi dan keberanian dalam mengambil tindakan.",
            "ESFP": "ESFP (The Performer): Cocok sebagai Social Media Specialist, Digital Marketer, atau Event Coordinator yang membutuhkan kreativitas dan ekspresi.",
            "ENFP": "ENFP (The Campaigner): Cocok untuk peran seperti Innovation Manager, Startup Developer, atau Game Designer yang membutuhkan ide-ide kreatif.",
            "ENTP": "ENTP (The Visionary): Cocok untuk menjadi Business Analyst, Product Owner, atau Founder Startup dengan ide-ide inovatif dan pikiran terbuka.",
            "ESTJ": "ESTJ (The Supervisor): Cocok sebagai IT Manager, Database Administrator, atau Project Manager berkat keterampilan organisasi dan praktis.",
            "ESFJ": "ESFJ (The Provider): Cocok untuk peran seperti HR IT Specialist, Customer Support Lead, atau Training Specialist dengan keramahan dan kooperasi.",
            "ENFJ": "ENFJ (The Protagonist): Cocok untuk menjadi Team Leader IT, IT Consultant, atau Scrum Master yang membutuhkan karisma dan kemampuan memimpin.",
            "ENTJ": "ENTJ (The Commander): Sangat cocok untuk peran CIO, CTO, atau IT Strategist dengan kemampuan kepemimpinan strategis."
        }

        # Inisialisasi setiap pertanyaan menjadi probabilitas 1/16
        self.type_probabilities = {mbti_type: 1/16 for mbti_type in self.mbti_types}

        # Load Data Question
        data = DataFetcher("./data.csv")
        self.questions = data.data

    # Fungsi untuk mengupdate probabilitas
    def update_probabilities(self, answer_likelihoods):
        for mbti_type in self.mbti_types:
            # Mengambil nilai yang ada
            probability = self.type_probabilities[mbti_type]

            # Mengambil per type (16 type)
            for i, letter in enumerate(mbti_type):
                if letter in answer_likelihoods:
                    probability *= answer_likelihoods[letter]

            # Mengudpate nilai yang ada
            self.type_probabilities[mbti_type] = probability

        # Semua totalnya di jumlah
        total = sum(self.type_probabilities.values())
        if total > 0:
            # Looping satu per satu, dan score per type di bagi lagi dengan total untuk normalisasi
            for mbti_type in self.type_probabilities:
                self.type_probabilities[mbti_type] /= total

    # Mengambil nilai yang paling besar
    def get_most_probable_type(self):
        return max(self.type_probabilities, key=self.type_probabilities.get)

    # Print tampilan pertanyaan
    def run(self):
        print("Welcome to the Bayesian MBTI Test!")
        print("Answer each question from 1 (Strongly Disagree) to 5 (Strongly Agree).")

        for idx, (question, answer_likelihoods) in enumerate(self.questions):
            print(f"\nQuestion {idx+1}: {question}")
            while True:
                answer = int(input("Your answer (1-5): "))
                if answer in [1, 2, 3, 4, 5]:
                    break
                else:
                    print("Please enter a number between 1 and 5.")

            # Kalau ditemukan jawaban, maka update si probabilities
            if answer in answer_likelihoods:
                self.update_probabilities(answer_likelihoods[answer])
            else:
                print("Warning: No likelihood data for this answer. Skipping update.")

        # Mengambil probabilitas terbesar
        final_type = self.get_most_probable_type()
        description = self.mbti_descriptions.get(final_type, "Deskripsi tidak tersedia.")
        print(f"\nYour MBTI type is most likely: {final_type}")
        print(f"{description}")

if __name__ == "__main__":
    app = BayesianMBTIApp()
    app.run()