import type { ReactNode } from 'react';
import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  image: string; // Use PNG/SVG from static/img/
  description: ReactNode;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'AI-Powered Feedback',
    image: '/img/ai-feedback.png', // Placeholder; replace with actual image
    description: (
      <>
        Leverage OpenAI Whisper for speech-to-text and GPT-4 for detailed feedback, helping you improve your English speaking skills.
      </>
    ),
  },
  {
    title: 'Real-Time Analytics',
    image: '/img/analytics.png', // Placeholder; replace with actual image
    description: (
      <>
        Track your progress with sliding window analysis using Bytewax and Redpanda, providing insights into your performance trends.
      </>
    ),
  },
  {
    title: 'Telegram Integration',
    image: '/img/telegram.png', // Placeholder; replace with actual image
    description: (
      <>
        Practice seamlessly via voice messages in Telegram, with a user-friendly interface designed for TOEFL and interview prep.
      </>
    ),
  },
];

function Feature({ title, image, description }: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <img src={image} alt={title} className={styles.featureImage} />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): ReactNode {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}