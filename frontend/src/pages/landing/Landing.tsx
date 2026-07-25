import { Link, useNavigate } from 'react-router-dom';
import { motion, useInView } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';
import { 
  ArrowRight, 
  Brain, 
  BarChart3, 
  Shield, 
  Zap, 
  Sparkles,
  PlayCircle,
  Github,
  Twitter,
  Linkedin,
  Mail,
  Menu,
  X,
  CheckCircle,
  TrendingUp,
  Users,
  DollarSign,
  Star,
  Building2
} from 'lucide-react';
import { Button } from '@/components/ui/Button';
import { useAuth } from '@/contexts/AuthContext';
import { Badge } from '@/components/ui/Badge';

export const Landing = () => {
  const { enterDemoMode } = useAuth();
  const navigate = useNavigate();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const heroRef = useRef(null);
  const featuresRef = useRef(null);
  const isHeroInView = useInView(heroRef, { once: true });
  const isFeaturesInView = useInView(featuresRef, { once: true });

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleDemo = () => {
    enterDemoMode();
    navigate('/dashboard');
  };

  const features = [
    {
      icon: Brain,
      title: 'AI Forecasting',
      description: 'Predict future sales and demand with 95% accuracy using advanced machine learning algorithms.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: BarChart3,
      title: 'Advanced Analytics',
      description: 'Real-time business insights with beautiful charts, trends, and comprehensive performance tracking.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: Shield,
      title: 'Risk Management',
      description: 'Identify and mitigate business risks proactively with AI-powered risk assessment and alerts.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: Zap,
      title: 'Smart Automation',
      description: 'Intelligent recommendations and automated workflows to optimize your business operations.',
      color: 'from-orange-500 to-amber-500'
    },
    {
      icon: TrendingUp,
      title: 'Growth Insights',
      description: 'Discover growth opportunities with AI-driven insights and actionable recommendations.',
      color: 'from-red-500 to-rose-500'
    },
    {
      icon: Users,
      title: 'Customer Intelligence',
      description: 'Understand your customers better with AI-powered segmentation and behavior analysis.',
      color: 'from-indigo-500 to-purple-500'
    }
  ];

  const stats = [
    { value: '98%', label: 'Customer Satisfaction', icon: Users },
    { value: '50K+', label: 'Businesses Using', icon: Building2 },
    { value: '+', label: 'Revenue Tracked', icon: DollarSign },
    { value: '4.9★', label: 'Average Rating', icon: Star },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-primary/5">
      {/* Navigation */}
      <nav className={'fixed top-0 z-50 w-full transition-all duration-300 ' + (scrolled ? 'border-b bg-background/80 backdrop-blur-lg shadow-lg' : 'bg-transparent')}>
        <div className="container mx-auto flex h-16 items-center justify-between px-4">
          <Link to="/" className="flex items-center gap-2 group">
            <div className="rounded-lg bg-gradient-to-r from-primary to-purple-600 p-1.5 transition-all group-hover:scale-110">
              <Sparkles className="h-5 w-5 text-white" />
            </div>
            <span className="text-xl font-bold bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
              ProfitPilot
            </span>
            <Badge variant="outline" className="ml-2 text-[10px] font-medium border-primary/30 text-primary">
              AI Pro
            </Badge>
          </Link>

          <div className="hidden items-center gap-6 md:flex">
            <Link to="/features" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Features
            </Link>
            <Link to="/how-it-works" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              How It Works
            </Link>
            <Link to="/testimonials" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Testimonials
            </Link>
            <Link to="/faq" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              FAQ
            </Link>
            <Link to="/pricing" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Pricing
            </Link>
            <Link to="/about" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              About
            </Link>
            <Link to="/contact" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
              Contact
            </Link>
          </div>

          <div className="hidden items-center gap-3 md:flex">
            <Link to="/login">
              <Button variant="ghost" size="sm">Sign In</Button>
            </Link>
            <Link to="/register">
              <Button size="sm" className="bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90">
                Get Started
              </Button>
            </Link>
          </div>

          <button
            className="md:hidden"
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            {isMobileMenuOpen ? <X size={24} /> : <Menu size={24} />}
          </button>
        </div>
      </nav>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="fixed top-16 z-40 w-full bg-background/95 backdrop-blur-lg border-b md:hidden"
        >
          <div className="container mx-auto flex flex-col space-y-4 px-4 py-6">
            <Link to="/features" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              Features
            </Link>
            <Link to="/how-it-works" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              How It Works
            </Link>
            <Link to="/testimonials" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              Testimonials
            </Link>
            <Link to="/faq" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              FAQ
            </Link>
            <Link to="/pricing" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              Pricing
            </Link>
            <Link to="/about" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              About
            </Link>
            <Link to="/contact" className="text-sm hover:text-primary" onClick={() => setIsMobileMenuOpen(false)}>
              Contact
            </Link>
            <div className="flex flex-col gap-2 pt-4 border-t">
              <Link to="/login">
                <Button variant="outline" className="w-full">Sign In</Button>
              </Link>
              <Link to="/register">
                <Button className="w-full bg-gradient-to-r from-primary to-purple-600">Get Started</Button>
              </Link>
            </div>
          </div>
        </motion.div>
      )}

      {/* Hero Section */}
      <section ref={heroRef} className="relative pt-32 pb-20 overflow-hidden">
        <div className="absolute inset-0 opacity-30">
          <div className="absolute top-20 left-10 w-72 h-72 bg-primary/20 rounded-full blur-3xl animate-float" />
          <div className="absolute bottom-20 right-10 w-96 h-96 bg-purple-600/20 rounded-full blur-3xl animate-float" style={{ animationDelay: '2s' }} />
        </div>

        <div className="container mx-auto px-4 relative">
          <div className="flex flex-col items-center text-center">
            <motion.div
              ref={heroRef}
              initial={{ opacity: 0, y: 20 }}
              animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6 }}
              className="max-w-5xl"
            >
              <div className="mb-6 inline-flex items-center gap-2 rounded-full bg-primary/10 px-4 py-2 text-sm font-medium text-primary border border-primary/20">
                <Sparkles className="h-4 w-4" />
                AI-Powered Business Intelligence
              </div>

              <h1 className="mb-6 text-4xl font-bold tracking-tight sm:text-6xl md:text-7xl lg:text-8xl">
                ProfitPilot{' '}
                <span className="bg-gradient-to-r from-primary to-purple-600 bg-clip-text text-transparent">
                  AI Pro
                </span>
              </h1>

              <p className="mb-8 text-lg text-muted-foreground sm:text-xl max-w-3xl mx-auto">
                Autonomous Business Intelligence & Decision Platform powered by advanced AI.
                Make data-driven decisions with real-time insights, predictions, and automation.
              </p>

              <div className="flex flex-wrap justify-center gap-4">
                <Button
                  size="lg"
                  className="gap-2 bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 text-white shadow-lg hover:shadow-xl transition-all"
                  onClick={handleDemo}
                >
                  <PlayCircle className="h-5 w-5" />
                  Try Demo
                </Button>
                <Link to="/register">
                  <Button size="lg" variant="outline" className="gap-2 border-2 hover:bg-primary/5">
                    Get Started <ArrowRight className="h-4 w-4" />
                  </Button>
                </Link>
              </div>

              <div className="mt-6 flex flex-wrap justify-center gap-6 text-sm text-muted-foreground">
                <span className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  No credit card required
                </span>
                <span className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  Free forever demo
                </span>
                <span className="flex items-center gap-1">
                  <CheckCircle className="h-4 w-4 text-green-500" />
                  14-day free trial
                </span>
              </div>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 40 }}
              animate={isHeroInView ? { opacity: 1, y: 0 } : {}}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="mt-16 grid w-full max-w-4xl grid-cols-2 gap-4 sm:grid-cols-4"
            >
              {stats.map((stat, index) => (
                <div key={index} className="rounded-xl border bg-card/50 backdrop-blur-sm p-4 text-center">
                  <stat.icon className="mx-auto h-6 w-6 text-primary mb-2" />
                  <div className="text-2xl font-bold">{stat.value}</div>
                  <div className="text-xs text-muted-foreground">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="features" ref={featuresRef} className="py-20 bg-muted/30">
        <div className="container mx-auto px-4">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={isFeaturesInView ? { opacity: 1, y: 0 } : {}}
            transition={{ duration: 0.6 }}
            className="text-center mb-12"
          >
            <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
              Features
            </Badge>
            <h2 className="text-3xl font-bold mb-4">Everything you need to grow</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              AI-powered tools to make better business decisions, predict trends, and optimize operations.
            </p>
          </motion.div>

          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={isFeaturesInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="group rounded-xl border bg-card p-6 shadow-sm transition-all hover:shadow-lg hover:-translate-y-1"
              >
                <div className={'mb-4 rounded-lg bg-gradient-to-r ' + feature.color + ' p-3 w-fit group-hover:scale-110 transition-transform'}>
                  <feature.icon className="h-6 w-6 text-white" />
                </div>
                <h3 className="mb-2 font-semibold text-lg">{feature.title}</h3>
                <p className="text-sm text-muted-foreground">{feature.description}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="text-center mb-12">
            <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
              How It Works
            </Badge>
            <h2 className="text-3xl font-bold mb-4">Simple, powerful, effective</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Get started in minutes with our intuitive platform
            </p>
          </div>

          <div className="grid gap-8 md:grid-cols-3">
            {[
              { step: '1', title: 'Connect Your Data', desc: 'Integrate with your existing business data sources effortlessly.' },
              { step: '2', title: 'AI Analysis', desc: 'Our AI analyzes your data and generates actionable insights.' },
              { step: '3', title: 'Make Decisions', desc: 'Use AI-powered recommendations to make better business decisions.' },
            ].map((item, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={isFeaturesInView ? { opacity: 1, y: 0 } : {}}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="relative text-center"
              >
                <div className="mx-auto mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-gradient-to-r from-primary to-purple-600 text-2xl font-bold text-white">
                  {item.step}
                </div>
                <h3 className="mb-2 font-semibold">{item.title}</h3>
                <p className="text-sm text-muted-foreground">{item.desc}</p>
                {index < 2 && (
                  <div className="hidden md:block absolute top-8 left-[60%] w-[40%] border-t-2 border-dashed border-primary/30" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-primary/10 to-purple-600/10">
        <div className="container mx-auto px-4 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
              Get Started
            </Badge>
            <h2 className="text-3xl font-bold mb-4">Ready to transform your business?</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto mb-8">
              Start using AI-powered business intelligence today. Join thousands of businesses already growing with ProfitPilot AI Pro.
            </p>
            <div className="flex flex-wrap justify-center gap-4">
              <Button
                size="lg"
                className="gap-2 bg-gradient-to-r from-primary to-purple-600 hover:from-primary/90 hover:to-purple-600/90 text-white shadow-lg hover:shadow-xl transition-all"
                onClick={handleDemo}
              >
                <PlayCircle className="h-5 w-5" />
                Try Demo Now
              </Button>
              <Link to="/register">
                <Button size="lg" variant="outline" className="border-2 hover:bg-primary/5">
                  Create Account
                </Button>
              </Link>
            </div>
          </motion.div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t py-12 bg-background">
        <div className="container mx-auto px-4">
          <div className="grid gap-8 md:grid-cols-4">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Sparkles className="h-5 w-5 text-primary" />
                <span className="font-bold">ProfitPilot AI Pro</span>
              </div>
              <p className="text-sm text-muted-foreground">
                Autonomous Business Intelligence & Decision Platform
              </p>
              <div className="mt-4 flex gap-4">
                <Link to="#" className="text-muted-foreground hover:text-foreground">
                  <Twitter className="h-4 w-4" />
                </Link>
                <Link to="#" className="text-muted-foreground hover:text-foreground">
                  <Linkedin className="h-4 w-4" />
                </Link>
                <Link to="#" className="text-muted-foreground hover:text-foreground">
                  <Github className="h-4 w-4" />
                </Link>
                <Link to="#" className="text-muted-foreground hover:text-foreground">
                  <Mail className="h-4 w-4" />
                </Link>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Product</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link to="/features" className="hover:text-foreground">Features</Link></li>
                <li><Link to="/pricing" className="hover:text-foreground">Pricing</Link></li>
                <li><Link to="/how-it-works" className="hover:text-foreground">How It Works</Link></li>
                <li><Link to="/testimonials" className="hover:text-foreground">Testimonials</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Company</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link to="/about" className="hover:text-foreground">About</Link></li>
                <li><Link to="/contact" className="hover:text-foreground">Contact</Link></li>
                <li><Link to="/privacy" className="hover:text-foreground">Privacy</Link></li>
                <li><Link to="/terms" className="hover:text-foreground">Terms</Link></li>
              </ul>
            </div>

            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li><Link to="/faq" className="hover:text-foreground">FAQ</Link></li>
                <li><Link to="/security" className="hover:text-foreground">Security</Link></li>
                <li><Link to="/cookies" className="hover:text-foreground">Cookies</Link></li>
                <li><Link to="/contact" className="hover:text-foreground">Contact</Link></li>
              </ul>
            </div>
          </div>

          {/* Developer Information */}
          <div className="mt-8 border-t pt-8 text-center">
            <p className="text-sm text-muted-foreground">
              Developed by <span className="font-medium text-primary">Sahzad Alam Ansiri</span>
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              📧 <a href="mailto:sahazadalam14@gmail.com" className="hover:text-primary transition-colors">sahazadalam14@gmail.com</a>
              {' '}|{' '}
              📞 <a href="tel:+919740782053" className="hover:text-primary transition-colors">+91 9740782053</a>
            </p>
            <p className="mt-2 text-xs text-muted-foreground">
              © 2026 ProfitPilot AI Pro. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};
