"""
AI Prompt Template Library for SAOIS CLI
Provides 20+ curated prompt templates for common development scenarios
"""
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box
from rich.prompt import Prompt, Confirm

console = Console()

PROMPT_TEMPLATES = {
    "design_optimization": {
        "name": "🎨 Design Optimization",
        "category": "UI/UX",
        "description": "Improve visual design and user experience",
        "template": """Analyze and optimize the design of this project:

Project: {project_name}
Location: {project_path}

Please review:
1. **Visual Design**: Colors, typography, spacing, layout consistency
2. **User Experience**: Navigation flow, accessibility, mobile responsiveness
3. **Component Design**: Reusable components, design system adherence
4. **Performance**: Image optimization, CSS efficiency, animations

Provide specific recommendations with:
- What to change and why
- Code examples for improvements
- Before/after comparisons where helpful

Focus on modern, clean, professional design that follows best practices."""
    },
    
    "architecture_review": {
        "name": "🏗️ Architecture Review",
        "category": "Architecture",
        "description": "Review and improve code architecture",
        "template": """Perform a comprehensive architecture review:

Project: {project_name}
Location: {project_path}

Analyze:
1. **Project Structure**: File organization, folder hierarchy, separation of concerns
2. **Design Patterns**: Current patterns used, opportunities for improvement
3. **Scalability**: Can this handle growth? Bottlenecks?
4. **Maintainability**: Code clarity, documentation, technical debt
5. **Security**: Vulnerabilities, best practices, data protection
6. **Performance**: Optimization opportunities, caching strategies

Provide:
- Architecture diagram (if helpful)
- Specific refactoring recommendations
- Priority ranking (critical/important/nice-to-have)
- Implementation roadmap"""
    },
    
    "button_enhancement": {
        "name": "🔘 Button & CTA Enhancement",
        "category": "UI/UX",
        "description": "Improve buttons and call-to-action elements",
        "template": """Enhance all buttons and CTAs in this project:

Project: {project_name}
Location: {project_path}

Review and improve:
1. **Visual Design**: Colors, hover states, active states, disabled states
2. **Accessibility**: ARIA labels, keyboard navigation, focus indicators
3. **Micro-interactions**: Animations, loading states, success/error feedback
4. **Consistency**: Unified button styles across the app
5. **Conversion Optimization**: CTA text, placement, urgency

Provide:
- Updated button component code
- CSS/Tailwind classes for all states
- Animation examples (subtle, professional)
- A/B testing suggestions"""
    },
    
    "3d_background": {
        "name": "🌌 3D Animated Background",
        "category": "Visual Effects",
        "description": "Add stunning 3D animated backgrounds",
        "template": """Create a stunning 3D animated background:

Project: {project_name}
Location: {project_path}
Preferred style: {style}

Requirements:
1. **Technology**: Three.js, WebGL, or CSS 3D transforms
2. **Performance**: 60fps, optimized for mobile, lazy loading
3. **Customization**: Colors match brand, adjustable speed/intensity
4. **Accessibility**: Reduced motion support, fallback for older browsers
5. **Integration**: Easy to add to existing pages

Provide:
- Complete implementation code
- Performance optimization tips
- Customization options
- Browser compatibility notes

Style options: particles, waves, geometric, abstract, gradient mesh"""
    },
    
    "ai_agent_optimization": {
        "name": "🤖 AI Agent Optimization",
        "category": "AI/ML",
        "description": "Optimize AI agents and chatbots",
        "template": """Optimize the AI agent/chatbot in this project:

Project: {project_name}
Location: {project_path}

Improve:
1. **Prompt Engineering**: Better system prompts, context management
2. **Response Quality**: Accuracy, relevance, tone, personality
3. **Performance**: Response time, token optimization, caching
4. **Context Handling**: Memory management, conversation flow
5. **Error Handling**: Fallbacks, graceful degradation
6. **User Experience**: Loading states, streaming responses, retry logic

Provide:
- Optimized prompt templates
- Context management strategies
- Code improvements
- Testing scenarios"""
    },
    
    "ai_features": {
        "name": "✨ AI-Powered Features",
        "category": "AI/ML",
        "description": "Add cutting-edge AI features",
        "template": """Add AI-powered features to enhance this project:

Project: {project_name}
Location: {project_path}

Suggest and implement:
1. **Smart Suggestions**: Auto-complete, recommendations, predictions
2. **Natural Language**: Search, commands, data queries
3. **Content Generation**: Text, images, summaries
4. **Personalization**: User preferences, adaptive UI, smart defaults
5. **Automation**: Workflow automation, smart scheduling
6. **Analysis**: Sentiment analysis, data insights, anomaly detection

For each feature provide:
- Use case and value proposition
- Implementation approach (API, model, service)
- Code examples
- Cost/performance considerations"""
    },
    
    "performance_audit": {
        "name": "⚡ Performance Audit",
        "category": "Performance",
        "description": "Comprehensive performance optimization",
        "template": """Conduct a full performance audit:

Project: {project_name}
Location: {project_path}

Analyze:
1. **Load Time**: Initial load, time to interactive, largest contentful paint
2. **Bundle Size**: JavaScript, CSS, images, fonts
3. **Runtime Performance**: Frame rate, memory usage, CPU usage
4. **Network**: API calls, caching, compression
5. **Database**: Query optimization, indexing, connection pooling
6. **Rendering**: DOM size, reflows, repaints

Provide:
- Lighthouse/WebPageTest scores
- Specific bottlenecks identified
- Optimization recommendations with priority
- Before/after metrics
- Implementation code"""
    },
    
    "accessibility_review": {
        "name": "♿ Accessibility (A11y) Review",
        "category": "Accessibility",
        "description": "Ensure WCAG 2.1 AA compliance",
        "template": """Comprehensive accessibility review:

Project: {project_name}
Location: {project_path}

Check for WCAG 2.1 AA compliance:
1. **Keyboard Navigation**: Tab order, focus management, shortcuts
2. **Screen Readers**: ARIA labels, semantic HTML, alt text
3. **Color Contrast**: Text, buttons, icons (4.5:1 minimum)
4. **Forms**: Labels, error messages, validation feedback
5. **Media**: Captions, transcripts, audio descriptions
6. **Responsive**: Works with zoom, text resize

Provide:
- Violations found with severity
- Code fixes for each issue
- Testing checklist
- Automated testing setup"""
    },
    
    "security_audit": {
        "name": "🔒 Security Audit",
        "category": "Security",
        "description": "Identify and fix security vulnerabilities",
        "template": """Security audit and hardening:

Project: {project_name}
Location: {project_path}

Review:
1. **Authentication**: JWT, sessions, password hashing, MFA
2. **Authorization**: Role-based access, permissions, API security
3. **Input Validation**: XSS, SQL injection, CSRF protection
4. **Data Protection**: Encryption, sensitive data handling, GDPR
5. **Dependencies**: Vulnerable packages, outdated libraries
6. **API Security**: Rate limiting, CORS, API keys
7. **Infrastructure**: HTTPS, headers, environment variables

Provide:
- Vulnerability report with severity ratings
- Fix recommendations with code
- Security best practices checklist
- Monitoring/logging suggestions"""
    },
    
    "mobile_optimization": {
        "name": "📱 Mobile Optimization",
        "category": "Mobile",
        "description": "Optimize for mobile devices",
        "template": """Optimize this project for mobile:

Project: {project_name}
Location: {project_path}

Improve:
1. **Responsive Design**: Breakpoints, flexible layouts, touch targets
2. **Performance**: Bundle size, lazy loading, image optimization
3. **Touch Interactions**: Gestures, swipe, pinch-to-zoom
4. **Mobile UX**: Navigation, forms, readability
5. **PWA Features**: Offline support, install prompt, push notifications
6. **Testing**: iOS Safari, Android Chrome, various screen sizes

Provide:
- Mobile-first CSS/components
- Touch interaction code
- Performance optimizations
- PWA implementation guide"""
    },
    
    "database_optimization": {
        "name": "🗄️ Database Optimization",
        "category": "Backend",
        "description": "Optimize database queries and schema",
        "template": """Database optimization review:

Project: {project_name}
Location: {project_path}
Database: {database_type}

Optimize:
1. **Schema Design**: Normalization, relationships, data types
2. **Indexes**: Missing indexes, unused indexes, composite indexes
3. **Queries**: N+1 problems, slow queries, query optimization
4. **Caching**: Query caching, result caching, Redis integration
5. **Scaling**: Sharding, replication, connection pooling
6. **Monitoring**: Slow query log, performance metrics

Provide:
- Schema improvements
- Index recommendations
- Query rewrites
- Caching strategy
- Migration scripts"""
    },
    
    "api_design": {
        "name": "🔌 API Design & Documentation",
        "category": "Backend",
        "description": "Design RESTful/GraphQL APIs",
        "template": """Design and document API:

Project: {project_name}
Location: {project_path}
API Type: {api_type}

Create:
1. **Endpoints**: RESTful routes or GraphQL schema
2. **Request/Response**: Data structures, validation, error handling
3. **Authentication**: JWT, API keys, OAuth
4. **Versioning**: Strategy for API evolution
5. **Documentation**: OpenAPI/Swagger, examples, SDKs
6. **Testing**: Unit tests, integration tests, load tests

Provide:
- Complete API specification
- Implementation code
- Documentation (Swagger/GraphQL Playground)
- Client SDK examples
- Testing suite"""
    },
    
    "error_handling": {
        "name": "🚨 Error Handling & Logging",
        "category": "DevOps",
        "description": "Implement robust error handling",
        "template": """Implement comprehensive error handling:

Project: {project_name}
Location: {project_path}

Implement:
1. **Error Boundaries**: React error boundaries, global handlers
2. **User-Friendly Messages**: Clear, actionable error messages
3. **Logging**: Structured logging, log levels, context
4. **Monitoring**: Error tracking (Sentry, LogRocket), alerts
5. **Recovery**: Retry logic, fallbacks, graceful degradation
6. **Debugging**: Source maps, error context, stack traces

Provide:
- Error handling utilities
- Logging setup
- Monitoring integration
- User-facing error UI
- Testing error scenarios"""
    },
    
    "testing_strategy": {
        "name": "🧪 Testing Strategy",
        "category": "Testing",
        "description": "Comprehensive testing implementation",
        "template": """Create comprehensive testing strategy:

Project: {project_name}
Location: {project_path}

Implement:
1. **Unit Tests**: Components, functions, utilities (Jest, Vitest)
2. **Integration Tests**: API endpoints, database operations
3. **E2E Tests**: User flows, critical paths (Playwright, Cypress)
4. **Visual Regression**: Screenshot testing, component snapshots
5. **Performance Tests**: Load testing, stress testing
6. **Coverage**: Aim for 80%+ coverage on critical paths

Provide:
- Testing framework setup
- Example tests for each type
- CI/CD integration
- Coverage reporting
- Testing best practices"""
    },
    
    "seo_optimization": {
        "name": "🔍 SEO Optimization",
        "category": "Marketing",
        "description": "Improve search engine rankings",
        "template": """SEO optimization audit:

Project: {project_name}
Location: {project_path}

Optimize:
1. **Meta Tags**: Title, description, Open Graph, Twitter Cards
2. **Structured Data**: Schema.org markup, rich snippets
3. **Performance**: Core Web Vitals, page speed
4. **Content**: Keywords, headings, internal linking
5. **Technical SEO**: Sitemap, robots.txt, canonical URLs
6. **Mobile**: Mobile-first indexing, responsive design

Provide:
- Meta tag templates
- Structured data implementation
- Performance improvements
- Content recommendations
- Technical SEO checklist"""
    },
    
    "animation_polish": {
        "name": "🎬 Animation & Micro-interactions",
        "category": "UI/UX",
        "description": "Add delightful animations",
        "template": """Add polished animations and micro-interactions:

Project: {project_name}
Location: {project_path}

Implement:
1. **Page Transitions**: Smooth route changes, loading states
2. **Component Animations**: Enter/exit, hover, click feedback
3. **Scroll Animations**: Parallax, reveal on scroll, progress indicators
4. **Loading States**: Skeletons, spinners, progress bars
5. **Success/Error**: Confetti, shake, bounce, fade
6. **Performance**: 60fps, GPU acceleration, reduced motion

Provide:
- Animation library setup (Framer Motion, GSAP)
- Component examples
- Performance optimization
- Accessibility considerations
- Animation timing guidelines"""
    },
    
    "dark_mode": {
        "name": "🌙 Dark Mode Implementation",
        "category": "UI/UX",
        "description": "Add beautiful dark mode",
        "template": """Implement dark mode:

Project: {project_name}
Location: {project_path}

Create:
1. **Color System**: Light/dark palettes, semantic colors
2. **Theme Toggle**: Switch component, persistence, system preference
3. **Component Updates**: All components support both themes
4. **Images/Icons**: Adaptive graphics, SVG color adjustments
5. **Accessibility**: Contrast ratios, readability
6. **Smooth Transition**: Theme switching animation

Provide:
- Color palette (CSS variables/Tailwind)
- Theme provider setup
- Toggle component
- Updated components
- Testing checklist"""
    },
    
    "form_optimization": {
        "name": "📝 Form Optimization",
        "category": "UI/UX",
        "description": "Create user-friendly forms",
        "template": """Optimize forms for better UX:

Project: {project_name}
Location: {project_path}

Improve:
1. **Validation**: Real-time, clear error messages, success states
2. **UX**: Auto-focus, tab order, smart defaults, auto-save
3. **Accessibility**: Labels, ARIA, keyboard navigation
4. **Mobile**: Large touch targets, appropriate keyboards
5. **Multi-step**: Progress indicator, save progress, back/forward
6. **Submission**: Loading states, success feedback, error recovery

Provide:
- Form component library
- Validation utilities
- Accessibility implementation
- Mobile optimizations
- Testing scenarios"""
    },
    
    "code_refactoring": {
        "name": "♻️ Code Refactoring",
        "category": "Code Quality",
        "description": "Clean up and modernize code",
        "template": """Refactor code for better quality:

Project: {project_name}
Location: {project_path}

Refactor:
1. **Code Smells**: Long functions, duplicated code, complex conditionals
2. **Modern Patterns**: Hooks, composition, functional programming
3. **Type Safety**: TypeScript migration, proper typing
4. **Performance**: Memoization, lazy loading, code splitting
5. **Readability**: Clear naming, comments, documentation
6. **Testing**: Make code more testable

Provide:
- Refactoring plan with priorities
- Before/after code examples
- Breaking change warnings
- Testing strategy
- Migration guide"""
    },
    
    "deployment_setup": {
        "name": "🚀 Deployment & CI/CD",
        "category": "DevOps",
        "description": "Set up automated deployment",
        "template": """Set up deployment and CI/CD:

Project: {project_name}
Location: {project_path}
Platform: {platform}

Implement:
1. **Build Pipeline**: Automated builds, testing, linting
2. **Deployment**: Staging, production, rollback strategy
3. **Environment Variables**: Secure secrets management
4. **Monitoring**: Health checks, uptime monitoring, alerts
5. **Performance**: CDN, caching, compression
6. **Documentation**: Deployment guide, troubleshooting

Provide:
- CI/CD configuration (GitHub Actions, etc.)
- Deployment scripts
- Environment setup
- Monitoring setup
- Runbook for common issues"""
    }
}

def list_prompt_templates():
    """Show all available prompt templates."""
    console.print("\n[bold #00ffff]📚 AI Prompt Template Library[/bold #00ffff]\n")
    console.print("[dim]20+ curated prompts for common development scenarios[/dim]\n")
    
    # Group by category
    categories = {}
    for key, template in PROMPT_TEMPLATES.items():
        cat = template["category"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((key, template))
    
    for category, templates in sorted(categories.items()):
        console.print(f"\n[bold #ff00ff]{category}[/bold #ff00ff]")
        for key, template in templates:
            console.print(f"  [#00ffff]{template['name']}[/#00ffff]")
            console.print(f"    [dim]{template['description']}[/dim]")
    
    console.print("\n[dim]💡 Use `saois prompts <name>` to view a specific template[/dim]")
    console.print(f"[dim]💡 Use 'saois prompts browse' for interactive selection[/dim]")

def browse_prompts():
    """Interactive prompt template browser."""
    try:
        from .core.ui import ui

        ui.header()
    except Exception:
        pass
    console.print("[bold #00ffff]🔍 Browse Prompt Templates[/bold #00ffff]\n")
    
    # Create table
    table = Table(show_header=True, header_style="bold #ff00ff", border_style="#00ffff", box=box.ROUNDED)
    table.add_column("#", style="dim", width=3)
    table.add_column("Template", style="#00ffff")
    table.add_column("Category", style="dim")
    
    template_list = list(PROMPT_TEMPLATES.items())
    for i, (key, template) in enumerate(template_list, 1):
        table.add_row(str(i), template["name"], template["category"])
    
    console.print(table)
    console.print()
    
    choice = Prompt.ask("[#ff00ff]Select template number (or 'q' to quit)[/#ff00ff]")
    
    if choice.lower() == 'q':
        return
    
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(template_list):
            key, template = template_list[idx]
            show_prompt_template(key)
        else:
            console.print("[red]Invalid selection[/red]")
    except ValueError:
        console.print("[red]Invalid input[/red]")

def show_prompt_template(template_key, project_name=None, project_path=None):
    """Display a specific prompt template."""
    try:
        from .core.ui import ui
        from .core.registry import registry

        ui.header()
    except Exception:
        pass

    if template_key not in PROMPT_TEMPLATES:
        console.print(f"[red]Template '{template_key}' not found[/red]")
        list_prompt_templates()
        return
    
    template = PROMPT_TEMPLATES[template_key]
    
    console.print(f"[bold #00ffff]{template['name']}[/bold #00ffff]\n")
    console.print(f"[dim]Category: {template['category']}[/dim]")
    console.print(f"[dim]{template['description']}[/dim]\n")
    
    # Get project context if not provided
    if not project_name:
        try:
            from .core.registry import registry

            projects = registry.get_all()
        except Exception:
            projects = {}
        if projects:
            console.print("[dim]Select a project to customize this prompt:[/dim]")
            project_list = list(projects.items())
            for i, (name, _) in enumerate(project_list[:10], 1):
                console.print(f"  {i}. {name}")
            
            choice = Prompt.ask("\n[#ff00ff]Project number (or press Enter to skip)[/#ff00ff]", default="")
            if choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(project_list):
                    project_name, project_path = project_list[idx]
    
    # Fill in template variables
    prompt_text = template["template"]
    if project_name and project_path:
        prompt_text = prompt_text.format(
            project_name=project_name,
            project_path=project_path,
            style="modern, clean",  # Default
            api_type="REST",  # Default
            database_type="PostgreSQL",  # Default
            platform="Vercel"  # Default
        )
    else:
        prompt_text = prompt_text.replace("{project_name}", "[YOUR PROJECT NAME]")
        prompt_text = prompt_text.replace("{project_path}", "[PROJECT PATH]")
        prompt_text = prompt_text.replace("{style}", "[STYLE PREFERENCE]")
        prompt_text = prompt_text.replace("{api_type}", "[REST/GraphQL]")
        prompt_text = prompt_text.replace("{database_type}", "[DATABASE TYPE]")
        prompt_text = prompt_text.replace("{platform}", "[PLATFORM]")
    
    # Display prompt
    console.print("=" * 70)
    console.print("[bold #00ffff]📋 COPY THIS PROMPT:[/bold #00ffff]")
    console.print("=" * 70 + "\n")
    console.print(prompt_text)
    console.print("\n" + "=" * 70)
    console.print("[dim]Copy the text above and paste it into your AI tool[/dim]")
    console.print("=" * 70 + "\n")
    
    if Confirm.ask("[#ff00ff]Copy another template?[/#ff00ff]", default=False):
        browse_prompts()
