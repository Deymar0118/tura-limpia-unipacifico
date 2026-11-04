import { useLayoutEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import {LandingHeader} from '../components/LandingHeader'
import HeroSection from '../components/HeroSection'
import SolucionSection from '../components/SolucionSection'
import ContexSection from '../components/ContextSection'
import ImpactoMetas from '../components/ImpactoMetas'
import CaracteristicasSection from '../components/CaracteristicasSection'
import './LandingPage.css'

gsap.registerPlugin(ScrollTrigger)

function createLandingScrollAnimations() {
   gsap.timeline({ defaults: { ease: 'power3.out' } })
      .fromTo('.hero__badge', { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.6 })
      .fromTo('.hero__title', { opacity: 0, y: 25 }, { opacity: 1, y: 0, duration: 0.8 }, '-=0.35')
      .fromTo('.hero__description', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: 0.7 }, '-=0.5')
      .fromTo('.hero__actions', { opacity: 0, y: 15 }, { opacity: 1, y: 0, duration: 0.6 }, '-=0.42')
      .fromTo('.hero__checks > .hero__check', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.07 }, '-=0.42')
      .fromTo('.hero__preview', { opacity: 0, x: 28 }, { opacity: 1, x: 0, duration: 0.85, ease: 'power2.out' }, '-=0.75')
      .fromTo('.tura__doc', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: 0.4, stagger: 0.08 }, '-=0.4')
      .fromTo('.tura__figure', { opacity: 0 }, { opacity: 1, duration: 0.4 }, '-=0.4')

   gsap.fromTo(
     '.landing-section--how .landing-section__inner',
     { opacity: 0, y: 30 },
     {
      opacity: 1,
      y: 0,
      duration: 0.4,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.landing-section--how', start: 'top 78%', once: true },
     }
   )
    gsap.fromTo(
    '.landing-steps > .landing-step',
    { opacity: 0, y: 26 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.14,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.landing-steps', start: 'top 78%', once: true },
    }
   )
     gsap.fromTo(
    '.solucion',
    { opacity: 0, y: 30 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.solucion', start: 'top 70%', once: true },
    }
  )
   gsap.fromTo(
    '.solucion__tarjetas> .solucion__tarjeta',
    { opacity: 0, y: 26 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.12,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.solucion__tarjetas', start: 'top 70%', once: true },
    }
  )
  gsap.fromTo(
    '.landing-section--features',
    { opacity: 0, y: 0.30 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.landing-section--features', start: 'top 70%', once: true },
    }
  )
   gsap.fromTo(
    '.landing-section__features-grid > .landing-feature',
    { opacity: 0, y: 26 },
    {
      opacity: 1,
      y: 0,
      duration: 0.6,
      stagger: 0.12,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.landing-section__features-grid', start: 'top 70%', once: true },
    }
  )
    gsap.fromTo(
    '.impacto-metas',
    { opacity: 0, y: 0.30 },
    {
      opacity: 1,
      y: 0,
      duration: 0.4,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.impacto-metas', start: 'top 70%', once: true },
    }
  )
   gsap.fromTo(
    '.impacto-metas__grid > .impacto-metas__tarjeta',
    { opacity: 0, y: 26 },
    {
      opacity: 1,
      y: 0,
      duration: 0.4,
      stagger: 0.1,
      ease: 'power2.out',
      scrollTrigger: { trigger: '.impacto-metas__grid', start: 'top 75%', once: true },
    }
  )
}

function LandingPage() {
  const landingRef = useRef(null)

  useLayoutEffect(() => {
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (reduceMotion) return undefined

    const ctx = gsap.context(createLandingScrollAnimations, landingRef)

    const refreshOnLoad = () => ScrollTrigger.refresh()
    window.addEventListener('load', refreshOnLoad)

    return () => {
      window.removeEventListener('load', refreshOnLoad)
      ctx.revert()
    }
  }, [])

  return (
    <div className="landing-page" ref={landingRef}>
      <LandingHeader />
      <main>
        <HeroSection />
        <ContexSection />
        <SolucionSection />
        <CaracteristicasSection />
        <ImpactoMetas />
      </main>
    </div>
  )
}

export default LandingPage