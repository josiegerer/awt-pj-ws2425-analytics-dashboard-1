import random
from datetime import datetime, timedelta
import json
import uuid


class XAPIGenerator:
    def __init__(self):
        self.course_structure = {
            "Grundlagen der Baumpflege": {
                "materials": [
                    "Bäume schützen",
                    "Bäume kappen",
                    "Bäume ausdünnen",
                    "Baumkonservierung",
                    "Beratung zu Fragen rund um Bäume",
                    "Krankheits- und Schädlingsbekämpfung durchführen",
                    "Grünpflanzen pflanzen",
                    "Baumkrankheiten bekämpfen"
                ]
            },
            "Grundlagen des Kletterns": {
                "materials": [
                    "Auf Bäume klettern",
                    "Gefahren im Umgang mit Bäumen mindern",
                    "Mit Seilausrüstung Bäume erklimmen",
                    "Sicherheitsverfahren in großen Höhen befolgen"
                ]
            },
            "Grundlagen der Instandhaltung": {
                "materials": [
                    "Kettensäge bedienen",
                    "Forstwirtschaftliche Ausrüstung instand halten",
                    "Bei der Baumidentifizierung assistieren"
                ]
            }
        }

        self.test_pass_threshold = 0.7  # 70% to pass a test

    def generate_user_profile(self):
        """Generate a random user profile with learning preferences"""
        return {
            "study_frequency": random.randint(2, 7),  # days per week
            "study_duration": random.randint(30, 180),  # minutes per session
            "completion_rate": random.uniform(0.7, 1.0),  # probability of completing an activity
            "test_performance": random.uniform(0.6, 1.0),  # base test performance
        }
    
    def add_context(self, subcourse, material):
        """Generate a standard context structure for xAPI statements"""
        return {
            "contextActivities": {
                "parent": [
                    {
                        "id": "https://example.com/activities/learning-path-5678",
                        "definition": {
                            "name": {
                                "en": subcourse
                            }
                        }
                    }
                ]
            },
            "extensions": {
                "https://example.com/activities/extensions/course_id": "course-1234"
            },
            "platform": "Adaptive Learning Dashboard"
        }

    def generate_statement(self, user_id, verb, activity, timestamp, score=None, duration=None):
        """Generate a single xAPI statement"""
        statement = {
            "id": str(uuid.uuid4()),
            "actor": {
                "objectType": "Agent",
                "name": f"User_{user_id}",
                "mbox": f"mailto:user_{user_id}@example.com"
            },
            "verb": {
                "id": f"http://adlnet.gov/expapi/verbs/{verb}",
                "display": {"de-DE": verb}
            },
            "object": {
                "id": f"http://example.com/activities/{activity.replace(' ', '_')}",
                "definition": {
                    "name": {"de-DE": activity}
                }
            },
            "timestamp": timestamp.isoformat()
        }

        if score is not None:
            statement["result"] = {
                "score": {
                    "scaled": score,
                    "raw": int(score * 100),
                    "min": 0,
                    "max": 100
                }
            }
        
        

        if duration is not None:
            statement["result"] = statement.get("result", {})
            statement["result"]["duration"] = f"PT{duration}M"

        return statement

    def generate_learning_session(self, user_id, material, timestamp, duration):
        """Generate statements for a complete learning material session"""
        statements = []

        # Initialize learning material
        statements.append(self.generate_statement(
            user_id, "initialized", material, timestamp
        ))

        # Exit learning material
        exit_time = timestamp + timedelta(minutes=duration)
        statements.append(self.generate_statement(
            user_id, "exited", material, exit_time,
            duration=duration
        ))

        return statements, exit_time

    def generate_test_session(self, user_id, material, timestamp, score):
        """Generate statements for a complete test session"""
        statements = []
        test_name = f"Test: {material}"

        # Score the test
        statements.append(self.generate_statement(
            user_id, "scored", test_name, timestamp,
            score=score
        ))

        # Complete or fail based on threshold
        verb = "completed" if score >= self.test_pass_threshold else "failed"
        statements.append(self.generate_statement(
            user_id, verb, test_name,
            timestamp + timedelta(minutes=1),
            score=score
        ))

        return statements

    # Generates a complete learning journey for one user of type consistent leraner 
    def generate_user_journey(self, user_id, start_date, profile):
        """Generate a complete learning journey for one user"""
        statements = []
        current_date = start_date
        

        for subcourse, content in self.course_structure.items():
            # Started subcourse
            statements.append(self.generate_statement(
                user_id, "initialized", subcourse, current_date
            ))

            for material in content["materials"]:
                if random.random() < profile["completion_rate"]:
                    # Learning session
                    duration = random.randint(
                        int(profile["study_duration"] * 0.8),
                        int(profile["study_duration"] * 1.2)
                    )

                    # Generate learning material statements
                    material_statements, end_time = self.generate_learning_session(
                        user_id, material, current_date, duration
                    )
                    statements.extend(material_statements)

                    # Generate test statements
                    test_score = random.uniform(
                        profile["test_performance"] * 0.8,
                        profile["test_performance"] * 1.1
                    )
                    test_score = min(1.0, test_score)  # Cap at 1.0

                    test_statements = self.generate_test_session(
                        user_id, material, end_time, test_score
                    )
                    statements.extend(test_statements)

                # Advance time
                days_advance = 7 / profile["study_frequency"]
                current_date += timedelta(days=days_advance)

            # Exit subcourse
            statements.append(self.generate_statement(
                user_id, "exited", subcourse, current_date
            ))

        return statements
## Generate a Learnining Journey for one user of type inconsistent learner
   
    def generate_user_journey_of_inconsistent_learner(self, user_id, start_date, profile):
        statements = []
        
        current_date = start_date
        completed_materials = set()
        
        uncompleted_materials = {material for subcourse in self.course_structure.values() for material in subcourse["materials"]}
        while current_date < start_date + timedelta(days=90):  # Simulate up to 3 months
            material = random.choice(uncompleted_materials)   
            if random.random() < profile["completion_rate"]:
            # Learning session
             duration = random.randint(
                int(profile["study_duration"] * 0.5),
                int(profile["study_duration"] * 1.5)
            )
             
            if random.random() > 0.5:
            # Generate learning material statements
              material_statements, end_time = self.generate_learning_session(
                user_id, material, current_date, duration
               )
              statements.extend(material_statements)
            
            if random.random() > 0.8:
               self.generate_statement(
                   user_id, "searched", material, current_date 
               )
               statements.append(self.generate_statement(
                   user_id, "searched", material, current_date 
               ))
               
            if random.random() > 0.5:
            # Generate test statements
                test_score = random.uniform(
                profile["test_performance"] * 0.5,
                profile["test_performance"] * 1.5
)
                test_score = min(1.0, test_score)  # Cap at 1.0

                test_statements = self.generate_test_session(
                user_id, material, end_time, test_score)
                statements.extend(test_statements)

                if test_score >= self.test_pass_threshold:
                  uncompleted_materials.remove(material)
                  completed_materials.add(material)

            # Advance time
            days_advance = 7 / profile["study_frequency"]
            current_date += timedelta(days=days_advance)

        return statements


## Generate a Learnining Journey for  user of type dimiished Driver 

def generate_dataset(num_users=5, output_file="xapi_statements1.json"):
    """Generate complete dataset with multiple users"""
    generator = XAPIGenerator()
    all_statements = []

    # Generate data for each user
    for user_id in range(1, num_users + 1):
        # Random start date within last 3 months
        start_date = datetime.now() - timedelta(days=random.randint(0, 90))
        profile = generator.generate_user_profile()

        user_statements = generator.generate_user_journey(user_id, start_date, profile)
        all_statements.extend(user_statements)

    # Sort by timestamp
    all_statements.sort(key=lambda x: x["timestamp"])

    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_statements, f, ensure_ascii=False, indent=2)

    return all_statements


if __name__ == "__main__":
    # Generate data for 5 users
    statements = generate_dataset(num_users=1)
    print(f"Generated {len(statements)} xAPI statements")