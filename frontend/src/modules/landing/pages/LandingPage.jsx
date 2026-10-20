import { useLayoutEffect, useRef } from 'react'
import gsap from 'gsap'
import { ScrollTrigger } from 'gsap/ScrollTrigger'
import {LandingHeader} from '../components/LandingHeader'
import HeroSection from '../components/HeroSection'
import ImpactoMetas from '../components/ImpactoMetas'

gsap.registerPlugin(ScrollTrigger)

function createLandingScrollAnimations() {
    gsap.timeline({ defaults: { ease: 'power3.out' } })
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
    <div ref={landingRef}>
      <LandingHeader />
      <main>
        <HeroSection />
        <ImpactoMetas />
      </main>
    </div>
  )
}

export default LandingPage