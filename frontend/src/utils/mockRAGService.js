// Mock RAG Service for development purposes
// This simulates the backend API responses when the full backend is not available

const mockResponses = {
  "what is physical ai": {
    answer: "Physical AI, also known as embodied AI, is an approach to artificial intelligence that emphasizes the role of physical embodiment in the development of intelligent behavior. The core principle is that intelligence emerges not just from computational processes, but from the dynamic interaction between an agent and its physical environment. This perspective challenges the traditional view of intelligence as purely information processing, suggesting instead that the body and its interactions with the world play a crucial role in cognitive processes.",
    sources: ["Module 1: Foundations of Physical AI", "Physical AI Conceptual Framework"],
    confidence: 0.95
  },
  "what are the foundations of physical ai": {
    answer: "The foundations of Physical AI include: 1) Embodied Cognition - the idea that cognitive processes are deeply rooted in the body's interactions with the physical world, 2) The Sensorimotor Loop - a continuous cycle of sensing, processing, and acting that connects an agent to its environment, 3) Morphological Computation - the concept that the physical form of a system can contribute to its intelligence, and 4) Physical Grounding of Cognition - ensuring that cognitive processes are grounded in physical interactions with the world.",
    sources: ["Module 1: Foundations of Physical AI", "Embodied AI Principles"],
    confidence: 0.92
  },
  "sensing and perception": {
    answer: "Sensing and perception in Physical AI systems involve multiple modalities: visual perception using cameras and computer vision algorithms, tactile sensing through touch-sensitive surfaces and force sensors, proprioception for understanding the position and movement of body parts, auditory perception for sound processing, and multi-sensory integration to combine information from different sensory channels into coherent percepts. These systems often use deep learning approaches for pattern recognition and sensor fusion techniques to combine data from multiple sources.",
    sources: ["Module 2: Sensing & Perception in Robotics", "Sensor Fusion Techniques"],
    confidence: 0.89
  },
  "control systems": {
    answer: "Control systems in humanoid robotics typically involve hierarchical control architectures with multiple levels: high-level task planning that determines what actions to perform, mid-level trajectory generation that creates smooth movement paths, and low-level motor control that executes precise joint movements. These systems often use techniques like inverse kinematics for calculating joint angles, impedance control for compliant interaction with the environment, and feedback control loops to adjust movements based on sensory information.",
    sources: ["Module 3: Control & Actuation in Humanoid Robotics", "Robot Control Theory"],
    confidence: 0.91
  },
  "ai applications": {
    answer: "AI applications in humanoid robotics include: autonomous navigation and path planning, object recognition and manipulation, human-robot interaction and communication, learning from demonstration, adaptive behavior for changing environments, and social robotics applications for assistance and companionship. These applications leverage machine learning techniques including reinforcement learning, deep learning, and transfer learning to enable robots to perform complex tasks in real-world environments.",
    sources: ["Module 4: AI Reasoning & Applications in Robotics", "Humanoid Robotics Applications"],
    confidence: 0.93
  }
};

// Function to find the best matching response based on the question
function findBestResponse(question) {
  const lowerQuestion = question.toLowerCase();

  // Check for exact matches first
  for (const [key, response] of Object.entries(mockResponses)) {
    if (lowerQuestion.includes(key)) {
      return response;
    }
  }

  // If no exact match, return a general response
  return {
    answer: `Based on the Physical AI & Humanoid Robotics book content, ${question} is an important topic covered in the comprehensive guide. The book explains fundamental principles of Physical AI, sensing and perception systems, control mechanisms, and real-world applications in humanoid robotics. For detailed information, please refer to the relevant modules in the book.`,
    sources: ["Physical AI & Humanoid Robotics Book", "Comprehensive Guide"],
    confidence: 0.75
  };
}

// Mock API functions
export async function mockAskQuestion(question, selectedText = null) {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));

  const response = findBestResponse(question);
  return response;
}

export async function mockSelectedTextAsk(question, selectedText) {
  // Simulate network delay
  await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 1000));

  return {
    answer: `Based on the selected text "${selectedText || 'the provided context'}", I can provide the following information: ${question}. The Physical AI & Humanoid Robotics book covers this topic in detail, explaining how physical interaction with the environment shapes intelligent behavior in robotic systems.`,
    sources: ["Selected Text Context", "Physical AI & Humanoid Robotics Book"],
    confidence: 0.85
  };
}