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
        <HomepageFeatures />
        <section className={styles.section}>
          <div className="container">
            <h2>Why Speech Coach?</h2>
            <p>
              Speech Coach is a Telegram-based assistant designed to help users
              improve their spoken English through AI-powered feedback and
              real-time analytics. Built as a personal project to prepare for
              TOEFL and interviews, it showcases a modern microservices
              architecture and advanced data pipelines.
            </p>
            <img
              src="/img/architecture-diagram.svg"
              alt="System Architecture"
              className={styles.architectureImage}
            />
          </div>
        </section>
      </main>
    </Layout>
  );
}