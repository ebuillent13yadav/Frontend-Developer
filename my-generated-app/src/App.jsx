import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

function App() {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<HeroSection />} />
        <Route path="/about" element={<AboutSection />} />
        <Route path="/projects" element={<ProjectsSection />} />
        <Route path="/skills" element={<SkillsSection />} />
        <Route path="/contact" element={<ContactForm />} />
      </Routes>
      <Footer />
    </Router>
  );
}

function Header() {
  return (
    <header className="bg-gray-900 text-white p-4 flex justify-between items-center">
      <div className="flex space-x-4">
        <a href="/" className="text-lg font-semibold">Portfolio</a>
      </div>
      <nav className="space-x-4">
        <NavigationItem path="/" label="Home" />
        <NavigationItem path="/about" label="About" />
        <NavigationItem path="/projects" label="Projects" />
        <NavigationItem path="/skills" label="Skills" />
        <NavigationItem path="/contact" label="Contact" />
      </nav>
    </header>
  );
}

function Footer() {
  return (
    <footer className="bg-gray-900 text-white p-4 mt-auto">
      <div className="flex justify-center items-center space-x-4">
        <a href="#" className="text-sm">GitHub</a>
        <a href="#" className="text-sm">LinkedIn</a>
        <a href="#" className="text-sm">Twitter</a>
      </div>
    </footer>
  );
}

function NavigationItem({ path, label }) {
  return (
    <a href={path} className="text-gray-300 hover:text-white transition-colors duration-200">{label}</a>
  );
}

function HeroSection() {
  return (
    <section className="h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-pink-500 text-white">
      <div className="max-w-screen-md p-8">
        <h1 className="text-4xl font-bold mb-2">Welcome to My Portfolio</h1>
        <p className="text-xl mb-8">A showcase of my skills and projects.</p>
        {/* Add more content as needed */}
      </div>
    </section>
  );
}

function AboutSection() {
  return (
    <section className="py-20">
      <div className="max-w-screen-md mx-auto p-4 bg-white/10 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-4">About Me</h2>
        <p className="text-lg mb-8">
          I am a dedicated frontend developer with a passion for creating elegant and user-friendly interfaces. Here's a little bit about me.
        </p>
        {/* Add more content as needed */}
      </div>
    </section>
  );
}

function ProjectsSection() {
  return (
    <section className="py-20">
      <div className="max-w-screen-md mx-auto p-4 bg-white/10 rounded-lg shadow-lg flex flex-wrap -mx-4 justify-center">
        <Card title="Project 1" description="Description of Project 1" />
        <Card title="Project 2" description="Description of Project 2" />
        {/* Add more project cards as needed */}
      </div>
    </section>
  );
}

function SkillsSection() {
  return (
    <section className="py-20">
      <div className="max-w-screen-md mx-auto p-4 bg-white/10 rounded-lg shadow-lg flex flex-wrap -mx-4 justify-center">
        <Card title="Skill 1" description="Description of Skill 1" />
        <Card title="Skill 2" description="Description of Skill 2" />
        {/* Add more skill cards as needed */}
      </div>
    </section>
  );
}

function ContactForm() {
  return (
    <section className="py-20">
      <div className="max-w-screen-md mx-auto p-4 bg-white/10 rounded-lg shadow-lg">
        <h2 className="text-3xl font-bold mb-4">Contact Me</h2>
        {/* Add form elements and validation as needed */}
        <FormInput label="Name" name="name" />
        <FormInput label="Email" name="email" type="email" required />
        <FormInput label="Message" name="message" type="textarea" required />
        <button className="mt-4 bg-blue-500 text-white py-2 px-4 rounded">Submit</button>
      </div>
    </section>
  );
}

function Card({ title, description }) {
  return (
    <article className="w-full max-w-sm p-6 my-4">
      <h3 className="text-xl font-bold mb-2">{title}</h3>
      <p>{description}</p>
    </article>
  );
}

function FormInput({ label, name, type = "text", required = false }) {
  return (
    <div className="mb-4">
      <label htmlFor={name} className="block text-gray-700 font-bold mb-2">{label}</label>
      <input
        id={name}
        name={name}
        type={type}
        required={required}
        className="w-full p-2 border rounded"
      />
    </div>
  );
}

export default App;