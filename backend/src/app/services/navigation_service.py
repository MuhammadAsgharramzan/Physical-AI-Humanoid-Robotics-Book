import asyncio
import logging
from typing import List, Dict, Optional, Union
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger(__name__)

class LearningObjective(Enum):
    FOUNDATIONAL = "foundational"
    TECHNICAL = "technical"
    PRACTICAL = "practical"
    RESEARCH = "research"
    HOBBYIST = "hobbyist"

class NavigationStyle(Enum):
    LINEAR = "linear"
    MODULAR = "modular"
    CUSTOM = "custom"
    EXPEDITE = "expedite"  # Fast track for experienced learners

@dataclass
class NavigationPath:
    path_id: str
    name: str
    description: str
    modules: List[str]
    sections: List[str]
    estimated_duration: int  # in minutes
    difficulty_level: str
    learning_objectives: List[LearningObjective]
    navigation_style: NavigationStyle
    customized_for_user: bool = False

@dataclass
class UserLearningProfile:
    user_id: Optional[int] = None
    learning_objectives: List[LearningObjective] = None
    preferred_navigation_style: NavigationStyle = NavigationStyle.LINEAR
    technical_background: str = "beginner"  # beginner, intermediate, advanced
    time_availability: str = "flexible"  # limited, moderate, extensive, flexible
    interests: List[str] = None

class NavigationPathService:
    """Service for customizing navigation paths based on learning objectives"""

    def __init__(self):
        # Define standard paths for different learning objectives
        self.standard_paths = {
            "foundational": NavigationPath(
                path_id="foundational",
                name="Foundational Path",
                description="Comprehensive introduction to Physical AI and humanoid robotics fundamentals",
                modules=["Module 1", "Module 2", "Module 3", "Module 4"],
                sections=[
                    "introduction", "foundations", "sensing", "control",
                    "ai_reasoning", "applications", "conclusion"
                ],
                estimated_duration=480,  # 8 hours
                difficulty_level="beginner",
                learning_objectives=[LearningObjective.FOUNDATIONAL],
                navigation_style=NavigationStyle.LINEAR
            ),
            "technical": NavigationPath(
                path_id="technical",
                name="Technical Deep Dive",
                description="In-depth exploration of technical implementations and algorithms",
                modules=["Module 1", "Module 3", "Module 4"],
                sections=[
                    "technical_foundations", "control_algorithms",
                    "implementation_details", "advanced_ai", "case_studies"
                ],
                estimated_duration=360,  # 6 hours
                difficulty_level="advanced",
                learning_objectives=[LearningObjective.TECHNICAL],
                navigation_style=NavigationStyle.MODULAR
            ),
            "practical": NavigationPath(
                path_id="practical",
                name="Practical Applications",
                description="Focus on real-world applications and case studies",
                modules=["Module 2", "Module 3", "Module 4"],
                sections=[
                    "sensing_practice", "control_practice",
                    "real_world_applications", "case_studies", "implementation"
                ],
                estimated_duration=300,  # 5 hours
                difficulty_level="intermediate",
                learning_objectives=[LearningObjective.PRACTICAL],
                navigation_style=NavigationStyle.MODULAR
            ),
            "expedite": NavigationPath(
                path_id="expedite",
                name="Fast Track",
                description="Accelerated path for experienced learners",
                modules=["Module 1", "Module 4"],
                sections=["key_concepts", "advanced_applications", "conclusion"],
                estimated_duration=180,  # 3 hours
                difficulty_level="advanced",
                learning_objectives=[LearningObjective.FOUNDATIONAL, LearningObjective.TECHNICAL],
                navigation_style=NavigationStyle.EXPEDITE
            )
        }

        # Define module dependencies
        self.module_dependencies = {
            "Module 1": [],  # Foundation, no prerequisites
            "Module 2": ["Module 1"],  # Requires foundational knowledge
            "Module 3": ["Module 1", "Module 2"],  # Requires sensing knowledge
            "Module 4": ["Module 1", "Module 2", "Module 3"]  # Requires all previous
        }

        # Define section dependencies within modules
        self.section_dependencies = {
            "Module 1": [
                "introduction",
                "foundations",
                "embodied_cognition",
                "sensorimotor_loop",
                "morphological_computation",
                "symbol_grounding",
                "applications"
            ],
            "Module 2": [
                "introduction",
                "sensing_systems",
                "perception_algorithms",
                "sensor_integration",
                "applications"
            ],
            "Module 3": [
                "introduction",
                "control_systems",
                "balance_control",
                "locomotion",
                "manipulation",
                "humanoid_systems"
            ],
            "Module 4": [
                "introduction",
                "ai_reasoning",
                "learning_systems",
                "planning_decision_making",
                "real_world_applications"
            ]
        }

    async def get_standard_path(self, path_type: str) -> Optional[NavigationPath]:
        """
        Get a standard navigation path by type
        """
        return self.standard_paths.get(path_type.lower())

    async def customize_path_for_user(
        self,
        user_profile: UserLearningProfile
    ) -> NavigationPath:
        """
        Customize a navigation path based on user profile and learning objectives
        """
        # Start with a base path based on primary learning objective
        if user_profile.learning_objectives:
            primary_objective = user_profile.learning_objectives[0].value
            base_path = self.standard_paths.get(primary_objective)
        else:
            base_path = self.standard_paths["foundational"]  # Default

        if not base_path:
            base_path = self.standard_paths["foundational"]

        # Customize the path based on user profile
        customized_modules = await self._select_modules_for_user(
            user_profile, base_path.modules
        )

        customized_sections = await self._select_sections_for_user(
            user_profile, customized_modules
        )

        # Adjust duration based on user's technical background
        adjusted_duration = self._adjust_duration_for_background(
            base_path.estimated_duration, user_profile.technical_background
        )

        # Create customized path
        customized_path = NavigationPath(
            path_id=f"custom_{user_profile.user_id or 'anonymous'}_{hash(str(user_profile.__dict__)) % 10000}",
            name=f"Custom Path for {user_profile.technical_background.title()} Learner",
            description=self._generate_path_description(user_profile),
            modules=customized_modules,
            sections=customized_sections,
            estimated_duration=adjusted_duration,
            difficulty_level=user_profile.technical_background,
            learning_objectives=user_profile.learning_objectives or [LearningObjective.FOUNDATIONAL],
            navigation_style=user_profile.preferred_navigation_style,
            customized_for_user=True
        )

        return customized_path

    async def _select_modules_for_user(
        self,
        user_profile: UserLearningProfile,
        available_modules: List[str]
    ) -> List[str]:
        """
        Select modules based on user profile and learning objectives
        """
        selected_modules = []

        for module in available_modules:
            should_include = await self._should_include_module(module, user_profile)
            if should_include:
                # Check dependencies
                dependencies_met = await self._check_module_dependencies(module, selected_modules)
                if dependencies_met:
                    selected_modules.append(module)

        return selected_modules

    async def _should_include_module(self, module: str, user_profile: UserLearningProfile) -> bool:
        """
        Determine if a module should be included based on user profile
        """
        # If user has specific interests, prioritize relevant modules
        if user_profile.interests:
            # Map interests to likely relevant modules
            interest_to_modules = {
                "control": ["Module 3"],
                "sensing": ["Module 2"],
                "ai": ["Module 4"],
                "foundation": ["Module 1"],
                "practical": ["Module 3", "Module 4"],
                "theory": ["Module 1", "Module 4"]
            }

            for interest in user_profile.interests:
                for target_module, modules in interest_to_modules.items():
                    if target_module in interest.lower() and module in modules:
                        return True

        # For expedited learning, include fewer modules
        if user_profile.preferred_navigation_style == NavigationStyle.EXPEDITE:
            if user_profile.technical_background == "advanced":
                # Advanced users in expedited mode might skip foundational modules
                return module in ["Module 1", "Module 4"]  # Key concepts and applications
            else:
                # Others get a balanced selection
                return module in ["Module 1", "Module 2", "Module 4"]

        # Default: include all available modules
        return True

    async def _check_module_dependencies(self, module: str, selected_modules: List[str]) -> bool:
        """
        Check if module dependencies are satisfied
        """
        dependencies = self.module_dependencies.get(module, [])
        return all(dep in selected_modules for dep in dependencies)

    async def _select_sections_for_user(
        self,
        user_profile: UserLearningProfile,
        modules: List[str]
    ) -> List[str]:
        """
        Select sections based on user profile and selected modules
        """
        selected_sections = []

        for module in modules:
            module_sections = self.section_dependencies.get(module, [])

            # Adjust sections based on user's technical background
            if user_profile.technical_background == "beginner":
                # Include all sections for comprehensive learning
                selected_sections.extend(module_sections)
            elif user_profile.technical_background == "intermediate":
                # Skip some introductory sections, include main content
                selected_sections.extend(module_sections[1:])  # Skip introduction
            else:  # advanced
                # Focus on advanced sections, implementation details
                if user_profile.preferred_navigation_style == NavigationStyle.EXPEDITE:
                    # In expedited mode, only core sections
                    selected_sections.extend([module_sections[0], module_sections[-1]])  # Intro and conclusion
                else:
                    # Include advanced sections
                    selected_sections.extend(module_sections[2:])  # Skip intro and foundations

        return selected_sections

    def _adjust_duration_for_background(self, base_duration: int, background: str) -> int:
        """
        Adjust estimated duration based on user's technical background
        """
        if background == "beginner":
            return int(base_duration * 1.2)  # More time needed
        elif background == "advanced":
            return int(base_duration * 0.8)  # Less time needed
        else:  # intermediate
            return base_duration

    def _generate_path_description(self, user_profile: UserLearningProfile) -> str:
        """
        Generate a descriptive text for the customized path
        """
        objectives = [obj.value for obj in user_profile.learning_objectives] if user_profile.learning_objectives else ["foundational"]
        return f"Customized learning path for {user_profile.technical_background} learner with focus on {', '.join(objectives)} objectives, designed for {user_profile.time_availability} time availability."

    async def get_navigation_recommendations(
        self,
        user_profile: UserLearningProfile
    ) -> Dict[str, any]:
        """
        Get recommendations for navigation path customization
        """
        recommendations = {
            "recommended_path_type": "custom",
            "suggested_modules": [],
            "suggested_sections": [],
            "time_advice": "",
            "difficulty_advice": "",
            "customization_options": []
        }

        # Time-based recommendations
        if user_profile.time_availability == "limited":
            recommendations["time_advice"] = "Consider the expedited path for time-efficient learning"
            recommendations["customization_options"].append("expedite")
        elif user_profile.time_availability == "extensive":
            recommendations["time_advice"] = "You have time for comprehensive coverage"
            recommendations["customization_options"].append("comprehensive")
        else:
            recommendations["time_advice"] = "Moderate pace recommended"

        # Difficulty recommendations
        if user_profile.technical_background == "beginner":
            recommendations["difficulty_advice"] = "Start with foundational concepts before advancing"
        elif user_profile.technical_background == "advanced":
            recommendations["difficulty_advice"] = "You can skip introductory material if desired"
        else:
            recommendations["difficulty_advice"] = "Balanced approach recommended"

        return recommendations

    async def validate_path(self, path: NavigationPath) -> Dict[str, any]:
        """
        Validate a navigation path for consistency and completeness
        """
        validation_result = {
            "is_valid": True,
            "issues": [],
            "suggestions": [],
            "module_dependencies_met": True,
            "section_dependencies_met": True
        }

        # Check module dependencies
        for i, module in enumerate(path.modules):
            dependencies = self.module_dependencies.get(module, [])
            for dependency in dependencies:
                if dependency not in path.modules[:i]:
                    validation_result["is_valid"] = False
                    validation_result["module_dependencies_met"] = False
                    validation_result["issues"].append(f"Module {module} requires {dependency} which is not in the path or appears after")

        # Check if path covers learning objectives
        if path.learning_objectives:
            # This is a simplified check - in reality, you'd check content coverage
            validation_result["suggestions"].append("Ensure path content aligns with stated learning objectives")

        return validation_result

# Global instance of the navigation path service
navigation_service = NavigationPathService()