# Tutorial Notebook Guide

This guide explains how to use the `flood_damage_tutorial.ipynb` notebook to learn about the Flood Damage Calculation Library.

## Prerequisites

Before running the tutorial notebook, ensure you have:

1. **Processed JRC Data**: Run `python process_jrc_excel.py` to create the required data files
2. **Dependencies Installed**: Run `pip install -r requirements.txt`
3. **Jupyter Notebook**: Installed via the requirements or separately

## Starting the Tutorial

### Option 1: Jupyter Notebook
```bash
jupyter notebook flood_damage_tutorial.ipynb
```

### Option 2: JupyterLab
```bash
jupyter lab flood_damage_tutorial.ipynb
```

### Option 3: VS Code
Open the `.ipynb` file directly in VS Code with the Python extension.

## Tutorial Structure

The notebook is organized into the following sections:

### 1. Introduction
- Overview of the library features
- Key capabilities and data sources

### 2. Setup and Installation
- Environment setup
- Data verification
- Library import

### 3. Basic Usage
- Simple damage calculation example
- Understanding the result structure
- Basic visualization

### 4. Understanding the Data
- JRC damage functions exploration
- Maximum damage values by country
- Regional differences visualization

### 5. Advanced Features
- Multiple building types comparison
- Automatic region inference
- Country-specific calculations

### 6. Batch Processing
- Processing multiple locations
- Portfolio analysis
- Performance considerations

### 7. Uncertainty Analysis
- Understanding confidence intervals
- Standard deviations
- Risk assessment

### 8. Regional Comparisons
- Comparing damage functions across regions
- Geographic analysis
- Regional risk patterns

### 9. Practical Use Cases
- Real-world scenarios
- Property portfolio analysis
- Flood risk assessment

### 10. Best Practices
- Input validation
- Error handling
- Performance optimization

## Key Learning Outcomes

After completing the tutorial, you will understand:

- How to calculate flood damage for individual locations
- How to process multiple locations efficiently
- How to interpret uncertainty in damage estimates
- How to compare damage across different regions
- Real-world applications and best practices

## Common Issues and Solutions

### Issue: "JRC data not found"
**Solution**: Run `python process_jrc_excel.py` to process the Excel data first.

### Issue: Import errors
**Solution**: Ensure you're in the correct directory and run `pip install -r requirements.txt`.

### Issue: Plotting style warnings
**Solution**: Update matplotlib and seaborn to the latest versions.

### Issue: Memory issues with large datasets
**Solution**: Process data in smaller batches using the batch processing methods.

## Interactive Features

The notebook includes:

- **Interactive plots** showing damage functions by region
- **Comparison charts** for different building types
- **Maps** showing regional coverage (if geographic libraries are available)
- **Uncertainty visualizations** with confidence intervals

## Extending the Tutorial

You can extend the tutorial by:

1. **Adding your own locations**: Modify the example coordinates
2. **Testing different scenarios**: Change flood depths and building types
3. **Analyzing your region**: Focus on specific countries or regions
4. **Custom visualizations**: Create additional plots and analyses

## Data Files Required

The tutorial expects these processed data files in `./processed_jrc_data/`:

- `damage_functions_jrc.parquet` - JRC damage functions
- `max_damage_residential_jrc.parquet` - Residential maximum damages
- `max_damage_commercial_jrc.parquet` - Commercial maximum damages  
- `max_damage_industrial_jrc.parquet` - Industrial maximum damages
- `iso_table_jrc.parquet` - ISO country codes

## Performance Tips

- **First run**: The first cell execution may take longer as data is loaded
- **Large calculations**: Use batch processing for multiple locations
- **Memory usage**: Clear variables between large calculations if needed
- **Plotting**: Some visualizations may take time with large datasets

## Getting Help

If you encounter issues:

1. Check that all data files are present and properly formatted
2. Verify all dependencies are installed
3. Restart the kernel and run cells in order
4. Check the main README.md for additional troubleshooting

## Next Steps

After completing the tutorial:

1. Explore the API documentation in the README
2. Try the library with your own data
3. Consider contributing improvements or examples
4. Apply the library to real flood risk assessment projects

---

**Happy Learning!** 🌊📊