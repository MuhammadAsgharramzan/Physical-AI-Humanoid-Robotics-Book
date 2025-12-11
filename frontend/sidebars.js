// @ts-check

// This runs in Node.js - Don't use client-side code here (browser APIs, JSX...)

/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.

 @type {import('@docusaurus/plugin-content-docs').SidebarsConfig}
 */
const sidebars = {
  // Physical AI & Humanoid Robotics Book Sidebar
  physicalAISidebar: [
    {
      type: 'category',
      label: 'Physical AI & Humanoid Robotics Book',
      collapsed: false,
      items: [
        'index', // Homepage
        {
          type: 'category',
          label: 'Module 1: Foundations of Physical AI',
          collapsed: false,
          items: [
            'module1_bilingual'
          ],
        },
        {
          type: 'category',
          label: 'Module 2: Sensing and Perception in Physical AI',
          collapsed: false,
          items: [
            'module2_bilingual'
          ],
        },
        {
          type: 'category',
          label: 'Module 3: Control and Locomotion Systems',
          collapsed: false,
          items: [
            'module3_bilingual'
          ],
        },
        {
          type: 'category',
          label: 'Module 4: Applications and Future Directions',
          collapsed: false,
          items: [
            'module4_bilingual'
          ],
        },
      ],
    },
  ],
};

export default sidebars;
