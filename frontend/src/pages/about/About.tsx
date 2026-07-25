import { motion } from 'framer-motion';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';
import { 
  Users, Target, Award, Globe, 
  Mail, Phone, MapPin, Linkedin,
  Github, Twitter, Sparkles
} from 'lucide-react';
import { Link } from 'react-router-dom';

export const About = () => {
  const team = [
    {
      name: 'Sahzad Alam Ansiri',
      role: 'Founder & Lead Developer',
      email: 'sahazadalam14@gmail.com',
      phone: '+91 9740782053',
      bio: 'Passionate about AI and Business Intelligence. Building the future of autonomous decision platforms.',
      avatar: 'SA'
    }
  ];

  const values = [
    {
      icon: Users,
      title: 'User First',
      description: 'We put our users at the center of everything we build.'
    },
    {
      icon: Target,
      title: 'Innovation',
      description: 'Constantly pushing boundaries with cutting-edge AI technology.'
    },
    {
      icon: Award,
      title: 'Excellence',
      description: 'Committed to delivering the highest quality solutions.'
    },
    {
      icon: Globe,
      title: 'Global Impact',
      description: 'Building solutions that empower businesses worldwide.'
    }
  ];

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
      className="min-h-screen py-20 px-4"
    >
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-12">
          <Badge variant="outline" className="mb-4 border-primary/30 text-primary">
            About Us
          </Badge>
          <h1 className="text-4xl font-bold mb-4">Building the Future of Business Intelligence</h1>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            We're on a mission to democratize AI-powered business intelligence and help companies make better decisions.
          </p>
        </div>

        {/* Mission Section */}
        <div className="grid gap-8 md:grid-cols-2 mb-16">
          <Card>
            <CardContent className="p-6">
              <h3 className="text-2xl font-bold mb-4">Our Mission</h3>
              <p className="text-muted-foreground">
                To empower businesses of all sizes with autonomous AI intelligence that makes decision-making faster, 
                smarter, and more accurate. We believe that AI should be accessible to everyone, not just enterprises 
                with massive resources.
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <h3 className="text-2xl font-bold mb-4">Our Vision</h3>
              <p className="text-muted-foreground">
                A world where every business decision is backed by AI-powered insights. We envision a future where 
                entrepreneurs and business leaders can focus on strategy while our AI handles the data analysis, 
                predictions, and recommendations.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Values */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-8">Our Values</h2>
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {values.map((value, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.4, delay: index * 0.1 }}
                className="rounded-xl border bg-card p-6 text-center shadow-sm transition-all hover:shadow-lg"
              >
                <div className="mx-auto mb-4 rounded-full bg-primary/10 p-3 w-fit">
                  <value.icon className="h-6 w-6 text-primary" />
                </div>
                <h4 className="font-semibold mb-2">{value.title}</h4>
                <p className="text-sm text-muted-foreground">{value.description}</p>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Founder Section */}
        <div className="mb-16">
          <h2 className="text-3xl font-bold text-center mb-8">Meet the Founder</h2>
          <div className="max-w-2xl mx-auto">
            <Card className="transition-all hover:shadow-lg">
              <CardContent className="p-6 text-center">
                <div className="mx-auto mb-4 flex h-24 w-24 items-center justify-center rounded-full bg-gradient-to-r from-primary to-purple-600 text-3xl font-bold text-white">
                  {team[0].avatar}
                </div>
                <h3 className="text-2xl font-bold">{team[0].name}</h3>
                <p className="text-muted-foreground">{team[0].role}</p>
                <p className="mt-4 text-muted-foreground">{team[0].bio}</p>
                <div className="mt-4 flex flex-wrap justify-center gap-4">
                  <a href={'mailto:' + team[0].email} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
                    <Mail className="h-4 w-4" />
                    {team[0].email}
                  </a>
                  <a href={'tel:' + team[0].phone} className="flex items-center gap-2 text-sm text-muted-foreground hover:text-primary transition-colors">
                    <Phone className="h-4 w-4" />
                    {team[0].phone}
                  </a>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* CTA */}
        <div className="text-center bg-gradient-to-r from-primary/10 to-purple-600/10 rounded-xl p-8">
          <h3 className="text-2xl font-bold mb-4">Ready to Transform Your Business?</h3>
          <p className="text-muted-foreground mb-6">
            Join thousands of businesses already using ProfitPilot AI Pro.
          </p>
          <Link to="/register">
            <button className="px-6 py-3 bg-gradient-to-r from-primary to-purple-600 text-white rounded-lg hover:shadow-lg transition-all">
              Get Started Today
            </button>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};
