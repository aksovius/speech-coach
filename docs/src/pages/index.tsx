import React from 'react';
import clsx from 'clsx';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import styles from './index.module.css';
import HomepageFeatures from '../components/HomepageFeatures';

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title}`}
      description="Practice spoken English with AI-powered feedback via Telegram"
    >
      <header className={clsx('hero hero--primary', styles.heroBanner)}>
        <div className="container">
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro"
            >
              Get Started
            </Link>
            {/* <Link
              className="button button--secondary button--lg"
              to="https://github.com/aksovius/speech-coach"
            >
              View on GitHub
            </Link> */}
          </div>
        </div>
      </header>
      <main className="mainWrapper">
        <section className={styles.section}>
          <div className="container">
          <h2>Why Speech Coach?</h2>
              <p>
                Speech Coach is an AI-powered speaking coach that helps developers and tech professionals 
                improve their spoken English through structured feedback and real-world practice scenarios. 
                It provides automated speech recognition, lexical analysis, and constructive suggestions 
                based on actual use cases — from job interviews to team meetings.
              </p>
            <img
              src="/img/architecture-diagram.svg"
              alt="System Architecture"
              className={styles.architectureImage}
            />
              <p>
                Originally built to practice English for professional contexts, Speech Coach now serves as 
                a foundation for language coaching, continuous improvement, and AI-driven communication 
                support. Its backend is powered by a modern microservices architecture and real-time data pipelines, 
                with a flexible delivery channel — including but not limited to Telegram.
              </p>
          </div>
        </section>
      </main>
        <HomepageFeatures />
    </Layout>
  );
}