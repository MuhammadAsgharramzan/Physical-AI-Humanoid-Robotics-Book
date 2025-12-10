import asyncio
import logging
from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class ExampleType(Enum):
    TECHNICAL = "technical"
    PRACTICAL = "practical"
    THEORETICAL = "theoretical"
    CASE_STUDY = "case_study"
    HISTORICAL = "historical"

class UserInterest(Enum):
    TECHNICAL = "technical"
    PRACTICAL = "practical"
    HOBBYIST = "hobbyist"
    ACADEMIC = "academic"

@dataclass
class Example:
    id: str
    title: str
    description: str
    content: str
    example_type: ExampleType
    module: str
    difficulty_level: str  # "beginner", "intermediate", "advanced"
    tags: List[str]
    relevance_score: float = 0.0

@dataclass
class ExampleSelection:
    selected_examples: List[Example]
    selection_reasoning: str
    user_profile_match: float

class ExampleSelectionService:
    """Service for selecting examples based on user interests and profile"""

    def __init__(self):
        # Predefined examples for different modules and interests
        self.examples_database = [
            # Module 1 Examples
            Example(
                id="m1-t1",
                title="Embodied AI in Self-Driving Cars",
                description="How self-driving cars use embodied AI principles",
                content="Self-driving cars demonstrate embodied AI by integrating perception, decision-making, and action in real-time. The car's sensors continuously perceive the environment, the AI processes this information to make driving decisions, and the vehicle acts by controlling steering, acceleration, and braking. This sensorimotor loop allows the car to adapt to dynamic road conditions.",
                example_type=ExampleType.PRACTICAL,
                module="Module 1",
                difficulty_level="beginner",
                tags=["embodied AI", "autonomous vehicles", "real-world application"]
            ),
            Example(
                id="m1-t2",
                title="Morphological Computation in Human Legs",
                description="How human leg structure contributes to energy-efficient walking",
                content="Human legs demonstrate morphological computation through their physical structure. The natural compliance of joints, the spring-like properties of tendons, and the mass distribution of limbs all contribute to energy-efficient walking without requiring complex computational control. This physical design reduces the burden on the nervous system.",
                example_type=ExampleType.THEORETICAL,
                module="Module 1",
                difficulty_level="intermediate",
                tags=["morphological computation", "biomechanics", "efficiency"]
            ),
            Example(
                id="m1-t3",
                title="Symbol Grounding in Robot Perception",
                description="How robots connect abstract symbols to real-world experiences",
                content="Symbol grounding is crucial for robots to understand the world. Rather than manipulating abstract symbols, robots must ground their understanding in sensory experiences. For example, a robot learns the concept of 'red' through visual experiences of red objects, not by being programmed with a definition of redness.",
                example_type=ExampleType.TECHNICAL,
                module="Module 1",
                difficulty_level="advanced",
                tags=["symbol grounding", "perception", "cognition"]
            ),

            # Module 2 Examples
            Example(
                id="m2-t1",
                title="LIDAR in Autonomous Robots",
                description="How LIDAR sensors enable 3D mapping and navigation",
                content="LIDAR (Light Detection and Ranging) sensors emit laser pulses and measure the time for reflections to return, creating detailed 3D maps of the environment. This technology enables robots to perceive depth and navigate complex spaces with high precision.",
                example_type=ExampleType.PRACTICAL,
                module="Module 2",
                difficulty_level="beginner",
                tags=["LIDAR", "sensing", "navigation", "mapping"]
            ),
            Example(
                id="m2-t2",
                title="Computer Vision for Object Recognition",
                description="How robots identify and classify objects in their environment",
                content="Computer vision systems use convolutional neural networks to identify objects in camera images. The robot learns to recognize patterns and features that distinguish different objects, enabling it to interact appropriately with its environment.",
                example_type=ExampleType.TECHNICAL,
                module="Module 2",
                difficulty_level="intermediate",
                tags=["computer vision", "object recognition", "CNN", "perception"]
            ),

            # Module 3 Examples
            Example(
                id="m3-t1",
                title="Balance Control in Humanoid Robots",
                description="How robots maintain stability while walking or standing",
                content="Humanoid robots use sophisticated balance control algorithms like ZMP (Zero Moment Point) control to maintain stability. These systems continuously adjust the robot's center of mass and foot placement to prevent falls during dynamic movements.",
                example_type=ExampleType.PRACTICAL,
                module="Module 3",
                difficulty_level="intermediate",
                tags=["balance", "stability", "ZMP", "control systems"]
            ),
            Example(
                id="m3-t2",
                title="Case Study: Boston Dynamics Atlas",
                description="Analysis of one of the most advanced humanoid robots",
                content="Boston Dynamics' Atlas robot demonstrates state-of-the-art humanoid capabilities including dynamic walking, running, jumping, and manipulation. Its sophisticated control systems integrate perception, planning, and actuation to achieve remarkable mobility.",
                example_type=ExampleType.CASE_STUDY,
                module="Module 3",
                difficulty_level="intermediate",
                tags=["case study", "Atlas", "humanoid", "dynamic movement"]
            ),

            # Module 4 Examples
            Example(
                id="m4-t1",
                title="Reinforcement Learning for Robot Control",
                description="How robots learn optimal behaviors through trial and error",
                content="Reinforcement learning enables robots to learn complex behaviors by receiving rewards for successful actions. The robot explores different strategies and gradually learns optimal policies for tasks like walking, grasping, or navigation.",
                example_type=ExampleType.THEORETICAL,
                module="Module 4",
                difficulty_level="advanced",
                tags=["reinforcement learning", "policy learning", "optimization"]
            ),
            Example(
                id="m4-t2",
                title="Tesla Bot Development Approach",
                description="Tesla's approach to humanoid robot development",
                content="Tesla's Optimus robot leverages the company's expertise in computer vision and autonomy to develop a practical humanoid robot. The approach emphasizes cost-effective manufacturing and integration with existing AI technologies.",
                example_type=ExampleType.CASE_STUDY,
                module="Module 4",
                difficulty_level="beginner",
                tags=["case study", "Tesla Bot", "practical robotics"]
            )
        ]

    async def select_examples_for_user(
        self,
        user_interests: List[str],
        learning_level: str = "beginner",
        module: Optional[str] = None,
        count: int = 3
    ) -> ExampleSelection:
        """
        Select examples based on user interests and profile
        """
        # Filter examples based on user interests and learning level
        filtered_examples = []

        for example in self.examples_database:
            # Apply module filter if specified
            if module and example.module.lower() != module.lower():
                continue

            # Calculate relevance based on user interests
            interest_match_score = self._calculate_interest_match(example, user_interests)
            level_match_score = self._calculate_level_match(example, learning_level)

            # Combine scores
            combined_score = (interest_match_score * 0.7) + (level_match_score * 0.3)

            if combined_score > 0.3:  # Threshold for relevance
                example.relevance_score = combined_score
                filtered_examples.append(example)

        # Sort by relevance score (descending)
        filtered_examples.sort(key=lambda x: x.relevance_score, reverse=True)

        # Select top examples
        selected_examples = filtered_examples[:min(count, len(filtered_examples))]

        # Calculate overall match score
        if selected_examples:
            avg_match = sum(ex.relevance_score for ex in selected_examples) / len(selected_examples)
        else:
            avg_match = 0.0

        return ExampleSelection(
            selected_examples=selected_examples,
            selection_reasoning=f"Selected based on user interests: {user_interests}, learning level: {learning_level}",
            user_profile_match=avg_match
        )

    def _calculate_interest_match(self, example: Example, user_interests: List[str]) -> float:
        """
        Calculate how well an example matches user interests
        """
        if not user_interests:
            return 0.5  # Default score if no interests specified

        # Check if example type matches any user interest
        type_match = 0
        for interest in user_interests:
            if interest.lower() in [et.value for et in ExampleType]:
                if example.example_type.value == interest.lower():
                    type_match = 0.8
                    break

        # Check tag matches
        tag_matches = 0
        for interest in user_interests:
            for tag in example.tags:
                if interest.lower() in tag.lower():
                    tag_matches += 1

        tag_score = min(1.0, tag_matches * 0.2)  # Up to 0.6 for tag matches

        # Check content matches
        content_matches = 0
        for interest in user_interests:
            if interest.lower() in example.content.lower():
                content_matches += 1

        content_score = min(0.4, content_matches * 0.2)  # Up to 0.4 for content matches

        return (type_match * 0.4) + (tag_score * 0.4) + (content_score * 0.2)

    def _calculate_level_match(self, example: Example, user_level: str) -> float:
        """
        Calculate how well an example matches user learning level
        """
        level_mapping = {
            "beginner": {"beginner": 1.0, "intermediate": 0.7, "advanced": 0.3},
            "intermediate": {"beginner": 0.7, "intermediate": 1.0, "advanced": 0.7},
            "advanced": {"beginner": 0.3, "intermediate": 0.7, "advanced": 1.0}
        }

        if user_level in level_mapping:
            return level_mapping[user_level].get(example.difficulty_level, 0.0)
        else:
            return 0.5  # Default score for unknown levels

    async def get_examples_by_type(self, example_type: ExampleType, count: int = 5) -> List[Example]:
        """
        Get examples of a specific type
        """
        matching_examples = [
            ex for ex in self.examples_database
            if ex.example_type == example_type
        ]

        return matching_examples[:min(count, len(matching_examples))]

    async def search_examples(self, query: str, count: int = 5) -> List[Example]:
        """
        Search examples by keyword
        """
        query_lower = query.lower()
        matching_examples = []

        for example in self.examples_database:
            # Search in title, description, content, and tags
            search_fields = [
                example.title.lower(),
                example.description.lower(),
                example.content.lower()
            ] + [tag.lower() for tag in example.tags]

            for field in search_fields:
                if query_lower in field:
                    matching_examples.append(example)
                    break  # Don't add the same example multiple times

        return matching_examples[:min(count, len(matching_examples))]

# Global instance of the example selection service
example_service = ExampleSelectionService()