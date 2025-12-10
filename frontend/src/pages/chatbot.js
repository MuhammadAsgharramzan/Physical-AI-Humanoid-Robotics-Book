import React from 'react';
import Layout from '@theme/Layout';
import RAGChatbot from '../components/RAGChatbot';

function ChatbotPage() {
  return (
    <Layout title="Book Assistant" description="Interactive Q&A with the Physical AI & Humanoid Robotics book content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <h1>Physical AI & Humanoid Robotics Book Assistant</h1>
            <p>
              Ask questions about the book content and get answers powered by Retrieval-Augmented Generation (RAG).
              Select text on any page and ask specific questions about it, or ask general questions about Physical AI and Humanoid Robotics.
            </p>

            <div style={{ maxWidth: '800px', margin: '0 auto' }}>
              <RAGChatbot />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ChatbotPage;