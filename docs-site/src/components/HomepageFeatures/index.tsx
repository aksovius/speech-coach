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
        Transform your voice into structured feedback using OpenAI Whisper for speech-to-text 
        and GPT-4 for tailored coaching. Go beyond scores — receive real linguistic insight.
      </>
    ),
  },
  {
    title: 'Real-Time Analytics',
    image: '/img/analytics.png', // Placeholder; replace with actual image
    description: (
      <>
        Understand your speaking with real metrics: total words, unique vocabulary, TTR, 
        sentence complexity, and active phrase usage. A quantified approach to language learning, 
        designed for developers and analytical minds.
      </>
    ),
  },
  {
    title: 'Telegram Integration',
    image: '/img/telegram.png', // Placeholder; replace with actual image
    description: (
      <>
        Built on a modern distributed architecture with FastAPI, Redpanda, and Bytewax. 
        Speech Coach is engineered for high availability, real-time processing, and future app integration.
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