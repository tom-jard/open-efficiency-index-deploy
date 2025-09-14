# Contributing to Open Efficiency Index

We welcome contributions to the Open Efficiency Index! This project aims to provide transparent alternatives to proprietary efficiency systems and advance energy efficiency data accessibility.

## 🎯 **Ways to Contribute**

### 🐛 **Report Issues**
- Data inconsistencies in appliance specifications
- Bugs in the web interface or API
- Regional data accuracy problems
- Performance issues

### 💡 **Suggest Features**  
- Additional appliance categories
- Enhanced regional data coverage
- API improvements
- User interface enhancements

### 📊 **Improve Data Quality**
- Validate efficiency calculations
- Add missing regional electricity data
- Enhance appliance specifications
- Contribute regional emissions factors

### 🌐 **Enhance Regional Coverage**
- Add utility-specific pricing data
- Improve grid emissions accuracy
- Expand to additional countries/regions
- Add time-of-use rate modeling

## 🚀 **Development Setup**

### **Prerequisites**
- Python 3.8+
- Modern web browser
- Git for version control

### **Local Development**
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/open-efficiency-index.git
cd open-efficiency-index

# Install dependencies
pip install -r requirements.txt

# Generate sample data
python scripts/data_pipeline.py

# Start development servers
python api/efficiency_api.py &
cd web && python -m http.server 8081
```

### **Testing Your Changes**
```bash
# Run system validation
python test_system_validation.py

# Test API endpoints
curl "http://localhost:8080/search?category=refrigerators&limit=5"

# Validate web interface
open http://localhost:8081/
```

## 📝 **Development Process**

### **1. Fork & Branch**
- Fork the repository to your GitHub account
- Create a feature branch: `git checkout -b feature-name`
- Use descriptive branch names: `fix-energy-display`, `add-heat-pump-data`

### **2. Make Changes**
- Follow existing code style and patterns
- Add comments for complex efficiency calculations
- Update documentation for user-facing changes
- Test thoroughly before submitting

### **3. Commit Guidelines**
```bash
# Use clear, descriptive commit messages
git commit -m "Fix energy display showing 0 values in web interface"
git commit -m "Add heat pump water heater efficiency calculations"
git commit -m "Update regional emissions factors with latest EPA data"
```

### **4. Submit Pull Request**
- Push changes to your fork
- Create a pull request with:
  - Clear description of changes
  - Reference to any related issues
  - Screenshots for UI changes
  - Test results confirmation

## 🔬 **Code Quality Standards**

### **Efficiency Calculations**
- All efficiency formulas must be clearly documented
- Use realistic performance thresholds, not artificial percentiles
- Separate intrinsic efficiency from regional impact
- Include unit tests for calculation functions

### **Data Processing**
- Validate data sources and methodology
- Handle missing or invalid data gracefully
- Log data quality issues for transparency
- Maintain data lineage documentation

### **API Development**
- Follow RESTful design principles
- Include comprehensive error handling
- Maintain backward compatibility
- Document all endpoints with examples

### **Frontend Development**
- Ensure responsive design across devices
- Maintain accessibility standards
- Use consistent design patterns
- Test with real data, not placeholder values

## 📊 **Data Quality Guidelines**

### **Appliance Specifications**
- Verify against official DOE/ENERGY STAR databases
- Flag outliers and suspicious values
- Document data source and collection date
- Validate efficiency calculations with multiple sources

### **Regional Data**
- Use official utility and government sources
- Update regularly to reflect current rates and emissions
- Document methodology for regional calculations
- Provide references for all data sources

### **Transparency Requirements**
- All algorithms must be open source and documented
- No proprietary or black-box calculations
- Clear methodology documentation required
- Reproducible results with provided data

## 🌍 **Regional Expansion**

### **Adding New Regions**
1. **Research local electricity markets and pricing structures**
2. **Gather official emissions factors for regional grid**
3. **Update regional calculation functions in data_pipeline.py**
4. **Add region to web interface dropdown options**
5. **Test calculations with realistic appliance data**
6. **Document sources and methodology**

### **International Expansion**
- Consider different efficiency standards (EU Energy Label, etc.)
- Account for voltage and frequency differences
- Research local appliance categories and specifications
- Adapt regional calculations for local markets

## 📞 **Getting Help**

### **Questions about Contributing**
- Open a [GitHub Discussion](https://github.com/yourusername/open-efficiency-index/discussions)
- Review existing [Issues](https://github.com/yourusername/open-efficiency-index/issues)
- Check the [documentation](documentation/README.md) for technical details

### **Reporting Security Issues**
For security-related issues, please email directly rather than opening a public issue.

### **Academic & Research Collaboration**
We welcome collaboration with:
- Energy policy researchers
- Appliance efficiency engineers  
- Utility industry professionals
- Environmental impact analysts
- Consumer advocacy organizations

## 🏆 **Recognition**

Contributors will be recognized in:
- Project documentation
- Research publication acknowledgments
- Conference presentations
- Academic collaborations

### **Types of Recognition**
- **Code Contributors**: GitHub contributor status
- **Data Contributors**: Credit in data source documentation
- **Research Contributors**: Co-authorship consideration for publications
- **Community Contributors**: Recognition in project communications

## 📄 **License**

By contributing to this project, you agree that your contributions will be licensed under the MIT License, ensuring open access to energy efficiency data and tools.

---

## 🌟 **Our Mission**

The Open Efficiency Index exists to make energy efficiency information transparent, accessible, and actionable for everyone. Your contributions directly advance:

- **Consumer empowerment** through honest efficiency information
- **Policy innovation** via open data and transparent methodology  
- **Environmental impact** by enabling informed appliance choices
- **Economic equity** through regional awareness and cost transparency

**Thank you for contributing to transparent energy efficiency standards!** 🏡✨