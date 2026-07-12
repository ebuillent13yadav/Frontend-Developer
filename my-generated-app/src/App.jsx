import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

const App = () => {
  return (
    <Router>
      <Header />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/about" element={<AboutMe />} />
        <Route path="/projects" element={<Projects />} />
        <Route path="/contact" element={<ContactForm />} />
      </Routes>
    </Router>
  );
};

const Header = () => (
  <header className="bg-black text-white p-4 flex justify-between items-center">
    <div className="logo">My Portfolio</div>
    <nav>
      <ul className="flex space-x-2">
        <li><LinkItem to="/">Home</LinkItem></li>
        <li><LinkItem to="/about">About Me</LinkItem></li>
        <li><LinkItem to="/projects">Projects</LinkItem></li>
        <li><LinkItem to="/contact">Contact</LinkItem></li>
      </ul>
    </nav>
  </header>
);

const LandingPage = () => (
  <main className="bg-gray-900 text-white p-12 flex justify-center items-center">
    <div className="max-w-screen-md">
      <Heading>Home</Heading>
      <Paragraph>Welcome to my portfolio. Explore my projects and learn more about me.</Paragraph>
    </div>
  </main>
);

const AboutMe = () => (
  <main className="bg-gray-900 text-white p-12 flex justify-center items-center">
    <div className="max-w-screen-md">
      <Heading>About Me</Heading>
      <Paragraph>I am a passionate React developer with a love for creating innovative solutions.</Paragraph>
    </div>
  </main>
);

const Projects = () => (
  <main className="bg-gray-900 text-white p-12 flex justify-center items-center">
    <div className="max-w-screen-md">
      <Heading>Projects</Heading>
      <ProjectList />
    </div>
  </main>
);

const ProjectCard = ({ title, description }) => (
  <article className="bg-gray-800 p-6 rounded-lg my-4 flex flex-col justify-between">
    <Heading>{title}</Heading>
    <Paragraph>{description}</Paragraph>
  </article>
);

const ProjectList = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
    <ProjectCard title="Project 1" description="Description of project 1." />
    <ProjectCard title="Project 2" description="Description of project 2." />
    <ProjectCard title="Project 3" description="Description of project 3." />
  </div>
);

const ContactForm = () => (
  <main className="bg-gray-900 text-white p-12 flex justify-center items-center">
    <div className="max-w-screen-md">
      <Heading>Contact Me</Heading>
      <form action="">
        <Paragraph>Your Name:</Paragraph>
        <FormInput name="name" />
        <Paragraph>Email:</Paragraph>
        <FormInput name="email" />
        <Paragraph>Message:</Paragraph>
        <FormInput name="message" />
        <Button type="submit">Send Message</Button>
      </form>
    </div>
  </main>
);

const LinkItem = ({ to, children }) => (
  <li><a href={to} className="text-white hover:text-gray-300">{children}</a></li>
);

const Heading = ({ children }) => <h1 className="text-2xl font-bold mb-4">{children}</h1>;

const Paragraph = ({ children }) => <p className="text-gray-300">{children}</p>;

const FormInput = ({ name, ...props }) => (
  <input type="text" name={name} className="w-full p-2 my-2 border rounded" {...props} />
);

const Button = ({ type, children }) => (
  <button type={type} className="bg-blue-500 text-white py-2 px-4 rounded">{children}</button>
);

export default App;