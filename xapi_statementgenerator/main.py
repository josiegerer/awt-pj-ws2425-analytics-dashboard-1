import random
from datetime import datetime, timedelta
import json
import uuid


#TODO: Create a difficulty for an activity

#TODO: Create a context for statement construction

#TODO: Add serach and reated verb for user journey

#TODO:

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
                ],
                "instructor": {
                    "mbox": "mailto:instructor2@example.com"
                }
                
            },
            "Grundlagen des Kletterns": {
                "materials": [
                    "Auf Bäume klettern",
                    "Gefahren im Umgang mit Bäumen mindern",
                    "Mit Seilausrüstung Bäume erklimmen",
                    "Sicherheitsverfahren in großen Höhen befolgen"
                ],
                "instructor": {
                    "mbox": "mailto:instructor1@example.com"
                }
            },
            "Grundlagen der Instandhaltung": {
                "materials": [
                    "Kettensäge bedienen",
                    "Forstwirtschaftliche Ausrüstung instand halten",
                    "Bei der Baumidentifizierung assistieren"
                ],
                "instructor": {
                    "mbox": "mailto:instructor3@example.com"
                }
            }
        }

        self.test_pass_threshold = 0.7  # 70% to pass a test

    def generate_user_profile(self):
        """Generate a random user profile with learning preferences"""
        return {
            "study_frequency": random.randint(2, 4),  # days per week (reduced for more spacing)
            "study_duration": random.randint(30, 180),  # minutes per session
            "completion_rate": random.uniform(0.7, 1.0),  # probability of completing an activity
            "test_performance": random.uniform(0.6, 1.0),  # base test performance
            # New parameters for enhanced learning patterns
            "min_sessions_before_test": random.randint(2, 3),
            "max_sessions_before_test": random.randint(4, 6),
            "preferred_study_time": {  # Time window when user typically studies
                "start_hour": random.randint(8, 14),
                "end_hour": random.randint(15, 20)
            }
        }
    
    def add_context(self, name, mbox):
        """Generate a standard context structure for xAPI statements"""
        return {
            "context": {
        "instructor": {
            "mbox": mbox,
            "name": name
        }
    }
        }

    def generate_statement(self, user_id, verb, activity, timestamp, score=None, duration=None, rating=None):
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
        if rating is not None:
            statement["result"] = {
                "score": {
                    "raw": int(rating),
                    "min": 1,
                    "max": 5
                }
            }
        
        if duration is not None:
            statement["result"] = statement.get("result", {})
            statement["result"]["duration"] = f"PT{duration}M"

        return statement

    def calculate_test_probability(self, session_count, profile):
        """Calculate probability of taking a test based on number of learning sessions"""
        min_sessions = profile["min_sessions_before_test"]
        max_sessions = profile["max_sessions_before_test"]

        if session_count < min_sessions:
            return 0.0
        elif session_count >= max_sessions:
            return 1.0
        else:
            # Linear increase in probability
            progress = (session_count - min_sessions) / (max_sessions - min_sessions)
            return progress * 0.8

    def get_next_study_date(self, current_date, profile):
        """Calculate the next study date based on user's frequency and preferences"""
        days_until_next = random.randint(1, 7 // profile["study_frequency"])
        next_date = current_date + timedelta(days=days_until_next)

        # Set time within user's preferred study window
        hour = random.randint(
            profile["preferred_study_time"]["start_hour"],
            profile["preferred_study_time"]["end_hour"]
        )
        minute = random.randint(0, 59)

        return next_date.replace(hour=hour, minute=minute)

    def generate_material_sessions(self, user_id, material, current_date, profile):
        """Generate multiple learning sessions for a material until test is passed"""
        statements = []
        session_count = 0
        test_passed = False

        while not test_passed:
            session_count += 1

            # Learning session
            duration = random.randint(
                int(profile["study_duration"] * 0.8),
                int(profile["study_duration"] * 1.2)
            )

            # Initialize material
            statements.append(self.generate_statement(
                user_id, "initialized", material, current_date
            ))

            # Exit material
            exit_time = current_date + timedelta(minutes=duration)
            statements.append(self.generate_statement(
                user_id, "exited", material, exit_time,
                duration=duration
            ))

            # Decide whether to take test
            test_probability = self.calculate_test_probability(session_count, profile)

            if random.random() < test_probability:
                # Add time gap before test (same day, but later)
                test_time = exit_time + timedelta(minutes=random.randint(60, 240))

                # Calculate test score with bonus for multiple sessions
                session_bonus = min(0.2, 0.05 * session_count)  # Max 20% bonus
                test_score = random.uniform(
                    profile["test_performance"] * 0.8,
                    profile["test_performance"] * 1.1
                ) + session_bonus
                test_score = min(1.0, test_score)

                # Generate test statements
                statements.append(self.generate_statement(
                    user_id, "scored", f"Test: {material}", test_time,
                    score=test_score
                ))

                verb = "completed" if test_score >= self.test_pass_threshold else "failed"
                statements.append(self.generate_statement(
                    user_id, verb, f"Test: {material}",
                    test_time + timedelta(minutes=random.randint(15, 30)),
                    score=test_score
                ))

                if test_score >= self.test_pass_threshold:
                    test_passed = True
                    # Next material starts on a different day
                    current_date = self.get_next_study_date(test_time, profile)
                else:
                    # Failed test - try again after a few days
                    current_date = self.get_next_study_date(test_time, profile)
            else:
                # Next session on a different day
                current_date = self.get_next_study_date(exit_time, profile)

        return statements, current_date

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

    #TODO: Generates a complete learning journey for one user of type consistent leraner 
    # Add more logic so the user has more than one lern sessions for a test
    # Time difference between learning session and test session should  exist
    # Time difference between two actions should exist
    # for each learning session the probability of make a test should get higher

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
                    # Generate all sessions for this material
                    material_statements, new_date = self.generate_material_sessions(
                        user_id, material, current_date, profile
                    )
                    statements.extend(material_statements)
                    current_date = new_date

                # Add time gap between materials
                current_date = self.get_next_study_date(current_date, profile)

            # Completed subcourse
            statements.append(self.generate_statement(
                user_id, "exited", subcourse, current_date
            ))

        return statements
    
## Generate a Learnining Journey for one user of type inconsistent learner 
    def generate_user_journey_of_inconsistent_learner(self, user_id, start_date, profile):
        """Generate a learning journey for an inconsistent learner"""
        statements = []
        current_date = start_date
        completed_materials = set()
        learning_sessions={}

        # Get a flat set of all materials across all subcourses
        uncompleted_materials = {material for subcourse in self.course_structure.values() for material in subcourse["materials"]}

        while current_date < start_date + timedelta(days=90):  # Simulate up to 3 months
            print(current_date)
            if not uncompleted_materials:  # If all materials are completed, break
                break

            # Randomly choose a material from uncompleted ones
            material = random.choice(list(uncompleted_materials))
            
            if random.random() < profile["completion_rate"]:  # User engages with the material
                duration = random.randint(
                    int(profile["study_duration"] * 0.5),
                    int(profile["study_duration"] * 1.5)
                )
                # Generate learning material statements
                if random.random() > 0.5:  # User spends time on the material
                    material_statements, end_time = self.generate_learning_session(
                        user_id, material, current_date, duration
                    )
                    if material not in learning_sessions:
                         learning_sessions[material] = 1
                         learning_sessions[material] += 0.1
                    current_date = end_time 
                    statements.extend(material_statements)
                

                # Occasionally add "searched" behavior
                if random.random() < 0.4:
                    statements.append(self.generate_statement(
                        user_id, "searched", material, current_date
                    ))

                # Generate test statements based on user behavior
                if random.random() > 0.5 * learning_sessions.get(material, 1):  # User takes a test
                    test_score = random.uniform(
                        profile["test_performance"] * 0.5,
                        profile["test_performance"] * 1.5
                    )
                    test_score = min(1.0, test_score)  # Cap at 1.0
                    current_date += timedelta(minutes=random.randint(10, 60))
                    test_statements = self.generate_test_session(
                        user_id, material, current_date, test_score
                    )
                    statements.extend(test_statements)

                    # Mark material as completed if the test is passed
                    if test_score >= self.test_pass_threshold:
                        uncompleted_materials.remove(material)
                        completed_materials.add(material)
                    
                    if random.random() < 0.4:
                       current_date += timedelta(minutes=random.randint(3, 10))
                       statements.append(self.generate_statement(
                        user_id, "rated", material, current_date
                    ))

            # Advance time based on study frequency
            days_advance = 7 / profile["study_frequency"]
            current_date += timedelta(days=days_advance)

        return statements



## TODO: Generate a Learnining Journey for user of type Diminished Drive  D
## Create a Logic so in the beginning the user is very active and then the user becomes less active (Samy)

    def generate_user_journey_of_diminished_drive_easy_quitter(self, user_id, start_date, profile):
        """
        Generates a learning journey for a user who starts highly motivated but whose engagement diminishes over time.
        
        Args:
            user_id (str): Identifier for the user.
            start_date (datetime): The starting date of the learning journey.
            profile (dict): User profile containing:
                            - "completion_rate": Probability of completing a material.
                            - "study_duration": Average study duration per session.
                            - "test_performance": Average performance in tests.
                            - "study_frequency": Frequency of study sessions per week.
                            
        Returns:
            list: A sequence of learning-related statements representing the user's journey.
        """
        statements = []
        current_date = start_date
        completed_materials = set()
        learning_sessions={}

        uncompleted_materials = {
            material for subcourse in self.course_structure.values() for material in subcourse["materials"]
        }

        diminishing_factor = 1.0  # User starts with full motivation
        diminishing_rate = 0.9  # Motivation diminishes by 10% each cycle

        while current_date < start_date + timedelta(days=90):  # Simulate up to 3 months
            print(uncompleted_materials)
            if not uncompleted_materials:
                # If all materials are completed or drive is too low, end simulation
                break
            
            # Adjust engagement by diminishing factor
            material = random.choice(list(uncompleted_materials))
            if random.random() < profile["completion_rate"] * diminishing_factor:
                # Learning session
                duration = random.randint(
                    int(profile["study_duration"] * 0.5 ),
                    int(profile["study_duration"] * 1.5 )
                )
                
                material_statements, end_time = self.generate_learning_session(
                    user_id, material, current_date, duration
                )
                if material not in learning_sessions:
                    learning_sessions[material] = 1
                    learning_sessions[material] += 0.1
                    
                statements.extend(material_statements)


                if random.random() < 0.5 * learning_sessions[material]:
                    # Test performance
                    test_score = random.uniform(
                        profile["test_performance"] * 0.5 * diminishing_factor,
                        profile["test_performance"] * 1.5 * diminishing_factor
                    )
                    test_score = min(1.0, test_score)  # Cap at 1.0

                    test_statements = self.generate_test_session(
                        user_id, material, end_time, test_score
                    )
                    statements.extend(test_statements)

                    if test_score >= self.test_pass_threshold:
                        uncompleted_materials.remove(material)
                        completed_materials.add(material)

            # Advance time
            days_advance = 7 / (profile["study_frequency"] * diminishing_factor)
            current_date += timedelta(days=days_advance)

            # Decrease motivation
            diminishing_factor *= diminishing_rate

        return statements


          

## TODO: Generate a Learnining Journey for user of type Diminished Drive C
## Create a Logic so in the beginning the user is very active and then the user becomes less active then the user becomes very active again
## First 4 weeks the user is very active, then the user becomes less active for 4-6 weeks and then the user becomes very active again for the last 4-2 weeks (Peter)

def generate_dataset(num_users=5, output_file="xapi_statements1.json"):
    """Generate complete dataset with multiple users"""
    generator = XAPIGenerator()
    all_statements = []

    # Generate data for each user
    for user_id in range(1, num_users + 1):
        # Random start date within last 3 months
        start_date = datetime.now() - timedelta(days=random.randint(0, 90))
        profile = generator.generate_user_profile()

        user_statements = generator.generate_user_journey_of_inconsistent_learner(user_id, start_date, profile)
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
    
    