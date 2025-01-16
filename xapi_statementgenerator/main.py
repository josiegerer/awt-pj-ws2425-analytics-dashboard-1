import random
from datetime import datetime, timedelta
import json
import uuid
from collections import defaultdict
import os

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
                    "mbox": "mailto:instructor2@example.com",
                    "name": "instructor2"
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
                    "mbox": "mailto:instructor1@example.com",
                    "name": "instructor1"
                }
            },
            "Grundlagen der Instandhaltung": {
                "materials": [
                    "Kettensäge bedienen",
                    "Forstwirtschaftliche Ausrüstung instand halten",
                    "Bei der Baumidentifizierung assistieren"
                ],
                "instructor": {
                    "mbox": "mailto:instructor3@example.com",
                    "name": "instructor3"
                }
            }
        }
    test_pass_threshold = 0.7  # 70% to pass a test
    
    
    def deep_merge(self,json1, json2):
        """
        Recursively merge two dictionaries.
        """
        for key, value in json2.items():
            if key in json1 and isinstance(json1[key], dict) and isinstance(value, dict):
                # Recursively merge nested dictionaries
                json1[key] = self.deep_merge(json1[key], value)
            else:
                # Overwrite or add key-value pairs
                json1[key] = value
        return json1


    
    def create_context(
    self,
    instructor_name: str,
    instructor_email: str,
    team_name: str = None,
    team_member_names: list = None,
    activity_name: str = None,
    activity_id: str = None,
    parent_activity_name: str = None,
    parent_activity_id: str = None,
    revision: str = None,
    platform: str = None,
    language: str = None
) -> dict:
        """
        Create a context JSON object for a learning record with customizable attributes.

        Parameters:
            instructor_name (str): Name of the instructor (required).
            instructor_email (str): Email of the instructor (required).
            team_name (str): Team name (optional).
            team_member_names (list): List of team member names (optional).
            activity_name (str): Name of the activity (optional).
            activity_id (str): ID of the activity (optional).
            parent_activity_name (str): Name of the parent activity (optional).
            parent_activity_id (str): ID of the parent activity (optional).
            revision (str): Revision identifier (optional).
            platform (str): Platform identifier (optional).
            language (str): Language (optional).

        Returns:
            dict: A context JSON object.
        """
        context = {
            "instructor": {
                "name": instructor_name,
                "mbox": f"mailto:{instructor_email}"
            }
        }

        # Add team details if provided
        if team_name or team_member_names:
            context["team"] = {
                "name": team_name or "Default Team",
                "member": [
                    {"name": name, "objectType": "Agent"} for name in (team_member_names or [])
                ],
                "objectType": "Group"
            }

        # Add context activities if provided
        context_activities = {}
        if activity_name or activity_id:
            context_activities["grouping"] = [
                {
                    "definition": {"name": {"en-US": activity_name or "Default Activity"}},
                    "id": activity_id or "http://example.com/default-activity",
                    "objectType": "Activity"
                }
            ]
        if parent_activity_name or parent_activity_id:
            context_activities["parent"] = [
                {
                    "id": parent_activity_id or "http://example.com/default-parent-activity",
                    "definition": {
                        "name": {"en": parent_activity_name or "Default Parent Activity"}
                    }
                }
            ]
        if context_activities:
            context["contextActivities"] = context_activities

        # Add optional attributes if provided
        if revision:
            context["revision"] = revision
        if platform:
            context["platform"] = platform
        if language:
            context["language"] = language

        return {"context": context}
    
    
    def get_difficulty_decimal(self, activity):
        # Define the difficulty ranges based on the alphabet
        difficulty_ranges = {
            1: "ABCDEF",
            2: "GHIJKL",
            3: "MNOPQR",
            4: "STUVWXYZ"
        }
        
        # Difficulty percentages in decimal form
        difficulty_decimals = {
            1: 0.15,
            2: 0.40,
            3: 0.30,
            4: 0.05,
            0: 0.00  # Default for short names or non-alphabetic characters
        }
        
        # Strip leading/trailing spaces from the activity
        activity = activity.strip()

        # Get the 7th letter (if the activity is shorter than 7 letters, assign a default difficulty)
        if len(activity) < 7:
            return difficulty_decimals[0]  # Default difficulty for short names

        seventh_letter = activity[6].upper()  # 6 because indexing starts at 0

        # Determine difficulty based on the 7th letter
        for difficulty, letters in difficulty_ranges.items():
            if seventh_letter in letters:
                return difficulty_decimals[difficulty]

        # Default difficulty if the 7th letter is not alphabetic
        return difficulty_decimals[0]


        

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
    
    def generate_statement_with_context(self,user_id, verb, activity, timestamp, score=None, duration=None, rating=None):
        return self.add_instructor_context(self.generate_statement(user_id, verb, activity, timestamp, score, duration, rating), activity)

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
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
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

    def get_next_study_date(self, current_date, profile, diminished_factor=1.0):
        """Calculate the next study date based on user's frequency and preferences"""
        # Convert to integer using floor division
        days_until_next = random.randint(1, int(7 // profile["study_frequency"] * diminished_factor) or 1)
        try:
            next_date = current_date + timedelta(days=days_until_next)
        except OverflowError:
            next_date = datetime.max

        # Set time within user's preferred study window
        hour = random.randint(
        profile["preferred_study_time"]["start_hour"],
        profile["preferred_study_time"]["end_hour"]
        )
        minute = random.randint(0, 59)

        return next_date.replace(hour=hour, minute=minute)


    def generate_material_sessions(self, user_id, material, current_date, profile):
        """Generate multiple learning sessions for a material until test is passed or max attempts reached"""
        statements = []
        session_count = 0
        test_passed = False
        MAX_SESSIONS = 10  # Maximum number of sessions before giving up
        
        while not test_passed and session_count < MAX_SESSIONS:
            session_count += 1

            # Possibly add search behavior before learning session
            if random.random() < 0.4:  # 40% chance to search
                statements.append(self.generate_statement_with_context(
                    user_id, "searched", material, current_date
                ))
            current_date += timedelta(minutes=random.randint(2, 5))

            # Learning session
            duration = random.randint(
                int(profile["study_duration"] * 0.8),
                int(profile["study_duration"] * 1.2)
            )

            # Initialize material
            statements.append(self.generate_statement_with_context(
                user_id, "initialized", material, current_date
            ))

            # Exit material
            exit_time = current_date + timedelta(minutes=duration)
            statements.append(self.generate_statement_with_context(
                user_id, "exited", material, exit_time,
                duration=duration
            ))

            # Possibly add rating after learning session
            if random.random() < 0.3:  # 30% chance to rate
                rate_time = exit_time + timedelta(minutes=random.randint(1, 5))
                statements.append(self.generate_statement_with_context(
                    user_id, "rated", material, rate_time,
                    rating=random.randint(1, 5)  # Added rating parameter
                ))
                exit_time = rate_time

            # Decide whether to take test
            test_probability = self.calculate_test_probability(session_count, profile)

            if random.random() < test_probability:
                # Add time gap before test (same day, but later)
                test_time = exit_time + timedelta(minutes=random.randint(60, 240))

                # Calculate test score with bonus for multiple sessions
                session_bonus = min(0.2, 0.05 * session_count)  # Max 20% bonus
                difficulty_decimal = self.get_difficulty_decimal(material)
                base_score = random.uniform(
                    profile["test_performance"] * 0.8,
                    profile["test_performance"] * 1.1
                )
                test_score = min(1.0, base_score - difficulty_decimal + session_bonus)

                # Generate test statements
                statements.append(self.generate_statement_with_context(
                    user_id, "scored", f"Test: {material}", test_time,
                    score=test_score
                ))

                verb = "completed" if test_score >= self.test_pass_threshold else "failed"
                statements.append(self.generate_statement_with_context(
                    user_id, verb, f"Test: {material}",
                    test_time + timedelta(minutes=random.randint(15, 30)),
                    score=test_score
                ))

                if test_score >= self.test_pass_threshold:
                    test_passed = True
                    current_date = self.get_next_study_date(test_time, profile)
                else:
                    # Failed test - try again after a few days
                    current_date = self.get_next_study_date(test_time, profile, diminished_factor=1.0)
            else:
                # Next session on a different day
                current_date = self.get_next_study_date(exit_time, profile)

            # If max sessions reached without passing, force completion
            if session_count == MAX_SESSIONS and not test_passed:
                final_test_time = current_date + timedelta(minutes=random.randint(60, 240))
                final_score = self.test_pass_threshold  # Ensure passing score
                statements.append(self.generate_statement_with_context(
                    user_id, "scored", f"Test: {material}", final_test_time,
                    score=final_score
                ))
                statements.append(self.generate_statement_with_context(
                    user_id, "completed", f"Test: {material}",
                    final_test_time + timedelta(minutes=random.randint(15, 30)),
                    score=final_score
                ))
                test_passed = True

        return statements, current_date

    def generate_learning_session(self, user_id, material, timestamp, duration):
        """Generate statements for a complete learning material session"""
        statements = []

        # Initialize learning material
        statements.append(self.generate_statement_with_context(
            user_id, "initialized", material, timestamp
        ))

        # Exit learning material
        exit_time = timestamp + timedelta(minutes=duration)
        statements.append(self.generate_statement_with_context(
            user_id, "exited", material, exit_time,
            duration=duration
        ))

        return statements, exit_time

    def generate_test_session(self, user_id, material, timestamp, score):
        """Generate statements for a complete test session"""
        test_name = f"Test: {material}"
        statements = [
            self.add_instructor_context(
                self.generate_statement(user_id, "scored", test_name, timestamp, score=score), material
            ),
            self.add_instructor_context(
                self.generate_statement(
                    user_id, 
                    "completed" if score >= self.test_pass_threshold else "failed", 
                    test_name, 
                    timestamp + timedelta(minutes=1), 
                    score=score
                ), 
                material
            )
        ]
        return statements

    

    def generate_user_journey_consistent(self, user_id, start_date, profile):
        """Generate a complete learning journey for one user with semi-random sequence"""
        statements = []
        current_date = start_date

        # Get materials grouped by subcourse for semi-random ordering
        materials_by_subcourse = {}
        for subcourse, content in self.course_structure.items():
            materials_by_subcourse[subcourse] = content["materials"].copy()
    	

        # Process materials with some randomness but maintaining some course structure
        while materials_by_subcourse:
            # Randomly select a subcourse that still has materials
            available_subcourses = [s for s, m in materials_by_subcourse.items() if m]
            if not available_subcourses:
                break

            subcourse = random.choice(available_subcourses)

            # Take 1-3 materials from this subcourse
            num_materials = min(random.randint(1, 3), len(materials_by_subcourse[subcourse]))
            for _ in range(num_materials):
                material = random.choice(materials_by_subcourse[subcourse])
                materials_by_subcourse[subcourse].remove(material)

                if random.random() < profile["completion_rate"]:
                    # Generate all sessions for this material
                    material_statements, new_date = self.generate_material_sessions(
                        user_id, material, current_date, profile
                    )
                    statements.extend(material_statements)
                    current_date = new_date

                # Add time gap between materials
                current_date = self.get_next_study_date(current_date, profile)

            # Remove subcourse if empty
            if not materials_by_subcourse[subcourse]:
                del materials_by_subcourse[subcourse]

        return statements
    
    def generate_user_journey_of_ushaped_learner(self, user_id, start_date, profile):
        """Generate a learning journey for a U-shaped learner (starts strong, declines, recovers)"""
        statements = []
        current_date = start_date
        # Get only the learning materials without subcourse structure
        uncompleted_materials = {material for subcourse in self.course_structure.values() for material in
                                 subcourse["materials"]}
        completed_materials = set()
        learning_sessions = {}

        # Calculate phase boundaries (3 phases over 90 days)
        phase_duration = timedelta(days=30)
        phase1_end = start_date + phase_duration
        phase2_end = phase1_end + phase_duration
        end_date = start_date + timedelta(days=90)

        while current_date < end_date and uncompleted_materials:
            # Determine current phase and adjust engagement
            if current_date < phase1_end:  # High engagement phase
                engagement_multiplier = 1.2
                study_frequency_modifier = 1
            elif current_date < phase2_end:  # Low engagement phase
                engagement_multiplier = 0.6
                study_frequency_modifier = 0.5
            else:  # Recovery phase
                engagement_multiplier = 1.3
                study_frequency_modifier = 1.2

            # Randomly search for any material (including completed ones)
            if random.random() < (0.4 * engagement_multiplier):
                search_material = random.choice(list(uncompleted_materials | completed_materials))
                current_date += timedelta(minutes=random.randint(1, 10))
                statements.append(self.generate_statement_with_context(
                    user_id, "searched", search_material, current_date
            ))
            current_date += timedelta(minutes=random.randint(2, 5))

            # Select material
            material = random.choice(list(uncompleted_materials))

            # Initialize learning sessions counter if needed
            if material not in learning_sessions:
                learning_sessions[material] = 0

            # Adjust engagement probability based on phase
            phase_engagement_rate = min(1.0, profile["completion_rate"] * engagement_multiplier)

            if random.random() < phase_engagement_rate:
                # Adjust study duration based on phase
                base_duration = profile["study_duration"]
                duration = random.randint(
                    int(base_duration * 0.5 * engagement_multiplier),
                    int(base_duration * 1.5 * engagement_multiplier)
                )

                # Learning session
                if random.random() < engagement_multiplier:
                    material_statements, end_time = self.generate_learning_session(
                        user_id, material, current_date, duration
                    )
                    learning_sessions[material] += 1
                    statements.extend(material_statements)
                    current_date = end_time

                    # Add search behavior more frequently during high engagement phases
                    if random.random() < (0.4 * engagement_multiplier):
                        current_date += timedelta(minutes=random.randint(3, 10))
                        statements.append(self.generate_statement_with_context(
                            user_id, "searched", material, current_date
                        ))

                    # Test taking probability increases with sessions and engagement
                    test_probability = self.calculate_test_probability(learning_sessions[material],
                                                                       profile) * engagement_multiplier

                    if random.random() < test_probability:
                        # Calculate test score based on sessions and phase
                        session_bonus = min(0.2, 0.05 * learning_sessions[material])
                        difficulty_decimal = self.get_difficulty_decimal(material)
                        base_performance = profile["test_performance"] * engagement_multiplier 

                        test_score = random.uniform(
                            base_performance * 0.8 - difficulty_decimal,
                            base_performance * 1.2 - difficulty_decimal
                        ) + session_bonus
                        test_score = min(1.0, test_score)

                        # Generate test statements
                        current_date += timedelta(minutes=random.randint(10, 60))
                        test_statements = self.generate_test_session(
                            user_id, material, current_date, test_score
                        )
                        statements.extend(test_statements)

                        # Handle test completion
                        if test_score >= self.test_pass_threshold:
                            uncompleted_materials.remove(material)
                            completed_materials.add(material)

                        # Add rating behavior
                        if random.random() < (0.4 * engagement_multiplier):
                            current_date += timedelta(minutes=random.randint(3, 10))
                            statements.append(self.generate_statement_with_context(
                                user_id, "rated", material, current_date,rating=random.randint(1, 5)
                            ))

            # Adjust time advancement based on phase
            base_advance = 7 / profile["study_frequency"]
            phase_advance = base_advance / study_frequency_modifier
            current_date = self.get_next_study_date(
                current_date + timedelta(days=random.uniform(0.5 * phase_advance, 1.5 * phase_advance)),
                profile
            )

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
            #print(current_date)
            if not uncompleted_materials:  # If all materials are completed, break
                break

            # Randomly choose a material from uncompleted ones
            material = random.choice(list(uncompleted_materials))
            
            if random.random() < profile["completion_rate"]:  # User engages with the material
               
                duration = random.randint(
                   int(profile["study_duration"] * 0.5 ),
                   int(profile["study_duration"] * 1.5 )
                )
                if material not in learning_sessions:
                         learning_sessions[material] = 0
                         
                # Generate learning material statements
                if random.random() > 0.5:  # User spends time on the material
                    material_statements, end_time = self.generate_learning_session(
                        user_id, material, current_date, duration
                    )
                    
                    learning_sessions[material] += 1
                    current_date = end_time 
                    statements.extend(material_statements)
                    
                    if random.random() < 0.05:
                       current_date += timedelta(minutes=random.randint(3, 10))
                       statements.append(self.generate_statement_with_context(
                        user_id, "rated", material, current_date,rating=random.randint(1, 5)
                    ))
                    
                

                # Occasionally add "searched" behavior
                if random.random() < 0.4:
                    current_date += timedelta(minutes=random.randint(3, 10))
                    statements.append(self.generate_statement_with_context(
                        user_id, "searched", material, current_date
                    ))

                # Generate test statements based on user behavior
                if random.random() < self.calculate_test_probability(learning_sessions[material],profile):  # User takes a test
                    session_bonus = min(0.2, 0.05 * learning_sessions[material])  # Max 20% bonus
                    difficulty_decimal = self.get_difficulty_decimal(material)
                    test_score = random.uniform(
                        profile["test_performance"] * 0.5 -difficulty_decimal,
                        profile["test_performance"] * 1.5 - difficulty_decimal
                    ) + session_bonus
                    
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
                       statements.append(self.generate_statement_with_context(
                        user_id, "rated", material, current_date,rating=random.randint(1, 5)
                    ))

            # Advance time based on study frequency
            
            current_date = self.get_next_study_date(current_date, profile)

        return statements
    def add_instructor_context(self, statement, material):
        """Add instructor context to a statement based on the material."""
        for subcourse, info in self.course_structure.items():
            if material in info["materials"]:
                instructor_info = info["instructor"]
                instructor_context = self.create_context(
                    instructor_name=instructor_info["name"],
                    instructor_email=instructor_info["mbox"].replace("mailto:", ""),
                    parent_activity_name=subcourse,
                    parent_activity_id=f"http://example.com/activities/{subcourse.replace(' ', '_')}"
                )
                self.deep_merge(statement, instructor_context)
                break
        return statement


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
            if not uncompleted_materials:
                # If all materials are completed or drive is too low, end simulation
                break
            
            # Adjust engagement by diminishing factor
            material = random.choice(list(uncompleted_materials))
            difficulty_decimal = self.get_difficulty_decimal(material)
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
                    learning_sessions[material] = 0
                    learning_sessions[material] += 1
                    
                statements.extend(material_statements)
                
                if random.random() > 0.4 * diminishing_factor:
                    current_date += timedelta(minutes=random.randint(3, 10))
                    statements.append(self.generate_statement_with_context(
                        user_id, "rated", material, current_date, rating=random.randint(1, 5)
                    ))
                
                if random.random() > 0.4 * diminishing_factor:
                    current_date += timedelta(minutes=random.randint(3, 10))
                    statements.append(self.generate_statement_with_context(
                        user_id, "searched", material, current_date
                    ))


                if random.random() < self.calculate_test_probability(learning_sessions[material], profile):
                    # Test performance
                    session_bonus = min(0.2, 0.05 * learning_sessions[material])
                    difficulty_decimal = self.get_difficulty_decimal(material)
                    
                    test_score = random.uniform(
                        (profile["test_performance"] * 0.5 * diminishing_factor)-difficulty_decimal,
                        (profile["test_performance"] * 1.5 * diminishing_factor)- difficulty_decimal
                    )+session_bonus
                    
                    test_score = min(1.0, test_score)  # Cap at 1.0

                    test_statements = self.generate_test_session(
                        user_id, material, end_time, test_score
                    )
                    statements.extend(test_statements)
                    
                    if random.random() > 0.4 * diminishing_factor:
                        current_date += timedelta(minutes=random.randint(3, 10))
                        statements.append(self.generate_statement_with_context(
                            user_id, "rated", material, current_date, rating=random.randint(1, 5)
                        ))

                    if test_score >= self.test_pass_threshold:
                        uncompleted_materials.remove(material)
                        completed_materials.add(material)

            # Advance time
            current_date = self.get_next_study_date(current_date, profile,diminished_factor=diminishing_factor)

            # Decrease motivation
            diminishing_factor *= diminishing_rate

        return statements
    


          

## TODO: Generate a Learnining Journey for user of type Diminished Drive C
## Create a Logic so in the beginning the user is very active and then the user becomes less active then the user becomes very active again
## First 4 weeks the user is very active, then the user becomes less active for 4-6 weeks and then the user becomes very active again for the last 4-2 weeks (Peter)

# def generate_dataset(num_users=5, output_file="xapi_statements1.json"):
#     """Generate complete dataset with multiple users"""
#     generator = XAPIGenerator()
#     all_statements = []

#     # Generate data for each user
#     for user_id in range(1, num_users + 1):
#         # Random start date within last 3 months
#         start_date = datetime.now() - timedelta(days=random.randint(0, 90))
#         profile = generator.generate_user_profile()

#         user_statements = generator.generate_user_journey_of_ushaped_learner(user_id, start_date, profile)
#         all_statements.extend(user_statements)

#     # Sort by timestamp
#     all_statements.sort(key=lambda x: x["timestamp"])

#     # Save to file
#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(all_statements, f, ensure_ascii=False, indent=2)

#     return all_statements


# if __name__ == "__main__":
#     # Generate data for 5 users
#     statements = generate_dataset(num_users=1)
#     print(f"Generated {len(statements)} xAPI statements")


def test_single_user_type(user_type):
    """Generate statements for a single user of specified type"""
    generator = XAPIGenerator()
    start_date = datetime.now() - timedelta(weeks=12)  # Start 12 weeks ago
    profile = generator.generate_user_profile()
    user_id = f"test_{user_type}_1"
    
    if user_type == "consistent":
        statements = generator.generate_user_journey_consistent(user_id, start_date, profile)
    elif user_type == "inconsistent":
        statements = generator.generate_user_journey_of_inconsistent_learner(user_id, start_date, profile)
    elif user_type == "u_shaped":
        statements = generator.generate_user_journey_of_ushaped_learner(user_id, start_date, profile)
    elif user_type == "diminished":
        statements = generator.generate_user_journey_of_diminished_drive_easy_quitter(user_id, start_date, profile)
    
    # Save to file
    # output_file = f"xapi_statements_{user_type}.json"
    # with open(output_file, 'w', encoding='utf-8') as f:
    #     json.dump(statements, f, ensure_ascii=False, indent=2)
    
    # print(f"Generated {len(statements)} statements for {user_type} learner")
    # return statements

    # Save to file in a directory relative to the script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "generated_data")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    output_file = os.path.join(output_dir, f"xapi_statements_{user_type}.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(statements, f, ensure_ascii=False, indent=2)
    
    print(f"Generated {len(statements)} statements for {user_type} learner")
    print(f"Saved to: {output_file}")
    return statements

def analyze_statements(statements):
    """Quick analysis of xAPI statements"""
    # Initialize analysis dict
    stats = {
        'total_statements': len(statements),
        'verbs': defaultdict(int),
        'scores': [],
        'materials': set()
    }
    
    # Analyze each statement
    for stmt in statements:
        # Count verbs
        verb = stmt['verb']['display']['de-DE']
        stats['verbs'][verb] += 1
        
        # Track materials
        material = stmt['object']['definition']['name']['de-DE']
        stats['materials'].add(material)
        
        # Collect scores
        if 'result' in stmt and 'score' in stmt['result']:
            score = stmt['result']['score'].get('scaled', 
                   stmt['result']['score'].get('raw', None))
            if score is not None:
                stats['scores'].append(score)
    
    # Print analysis
    print("\nQuick Analysis:")
    print(f"Total Statements: {stats['total_statements']}")
    print(f"Unique Materials: {len(stats['materials'])}")
    print("\nVerb Distribution:")
    for verb, count in stats['verbs'].items():
        print(f"  {verb}: {count}")
    if stats['scores']:
        avg_score = sum(stats['scores']) / len(stats['scores'])
        print(f"\nAverage Score: {avg_score:.2f}")

if __name__ == "__main__":
    # Test each type individually
    user_types = ["consistent", "inconsistent", "u_shaped", "diminished"]

    for utype in user_types:
        print(f"\nTesting {utype} learner:")
        statements = test_single_user_type(utype)
        analyze_statements(statements)
    
    