# Amazon Apparel Sales Dataset Cleaning Report

## Executive Summary

This report documents the comprehensive data cleaning process applied to the Amazon Apparel Sales dataset. The original dataset contained 37,432 entries with 10 columns, and through systematic cleaning and validation, the dataset was refined to 36,391 entries with 8 columns, ensuring data quality and consistency for downstream analysis.

---

## 1. Dataset Overview

### Initial State
- **Total Records**: 37,432 entries
- **Total Columns**: 10 columns
- **Data Types**: 1 integer column (index), 9 object columns
- **Memory Usage**: 2.9+ MB

### Columns in Original Dataset
1. `index` - Integer index column
2. `DATE` - Date information (object type)
3. `Months` - Month information (object type)
4. `CUSTOMER` - Customer names (object type)
5. `Style` - Product style codes (object type)
6. `SKU` - Stock Keeping Unit codes (object type)
7. `Size` - Product sizes (object type)
8. `PCS` - Pieces/quantity (object type)
9. `RATE` - Price rate (object type)
10. `GROSS AMT` - Gross amount (object type)

### Data Quality Issues Identified
- Missing values across multiple columns
- Inconsistent data formats (dates, months, sizes)
- Mixed data types in columns that should be numeric
- Misplaced data (customer names in date column, style codes in date column)
- Inconsistent capitalization and whitespace
- Non-standard size formats

---

## 2. Initial Data Preparation

### 2.1 Column Name Standardization
**Action**: Standardized all column names to lowercase and replaced spaces with underscores.

**Changes**:
- `DATE` → `date`
- `Months` → `months`
- `CUSTOMER` → `customer`
- `Style` → `style`
- `SKU` → `sku`
- `Size` → `size`
- `PCS` → `pcs`
- `RATE` → `rate`
- `GROSS AMT` → `gross_amt`

**Rationale**: Consistent naming conventions improve code readability and prevent errors from case sensitivity.

### 2.2 Index Column Removal
**Action**: Dropped the `index` column as it was redundant.

**Result**: Dataset reduced to 9 columns.

---

## 3. Date Column Cleaning

### 3.1 Missing Value Handling
**Initial State**: 37,431 non-null entries (1 missing value)

**Action**: Dropped the single row with missing date value.

**Result**: 37,431 entries remaining.

### 3.2 Data Type Conversion
**Action**: Attempted to convert date column to datetime format using format `'%m-%d-%y'`.

**Issue Discovered**: The date column contained non-date values including:
- Customer names (e.g., 'JNE3826', 'JNE3827', 'JNE3828')
- Style codes
- Special markers ('SKU', 'Style', 'CUSTOMER')

### 3.3 Data Recovery Strategy
**Problem**: Customer names and style codes were incorrectly placed in the date column, while actual dates were missing.

**Solution Implemented**:
1. **Identified misplaced data**: Separated date entries into two categories:
   - Entries with numbers (actual dates or style codes)
   - Entries without numbers (customer names)

2. **Style column imputation**: 
   - For date entries starting with a letter where style was null, filled style column with the date value
   - **Result**: 1,037 style observations were recovered

3. **Customer column imputation**:
   - For date entries without numbers where customer was null, filled customer column with the date value
   - **Result**: 2 customer observations were recovered

4. **Special markers handling**:
   - For entries containing 'SKU', 'Style', or 'CUSTOMER' in the date column, set customer to 'Unspecified'

**Impact**: This data recovery step significantly improved data completeness by utilizing misplaced information.

---

## 4. Months Column Cleaning

### 4.1 Missing Value Analysis
**Initial State**: 37,407 non-null entries (24 missing values)

**Investigation**: Examined rows with missing months values and found no meaningful data in other columns.

**Action**: Dropped all 24 rows with missing months values.

**Result**: 37,407 entries remaining.

### 4.2 Format Standardization
**Target Format**: 'Mon-YY' (e.g., 'Jun-21', 'Apr-22')

**Issues Found**:
- Mixed formats: Some entries were in date format ('03-09-22')
- Some entries were already in correct format ('Jun-21')
- Some entries were in incorrect formats

**Cleaning Steps**:

1. **Format Detection and Imputation**:
   - Created functions to identify correct format (`rformat`: 'Mon-YY') and date format (`wformat`: 'MM-DD-YY')
   - For rows with incorrect month formats:
     - If customer column had correct 'Mon-YY' format, used customer value
     - If date column had 'MM-DD-YY' format, used date value

2. **Date Format Conversion**:
   - Converted date-like formats ('MM-DD-YY') to month format ('Mon-YY')
   - Created month mapping: '01'→'Jan', '02'→'Feb', etc.
   - Applied conversion: '03-09-22' → 'Mar-22'

3. **Format Cleanup**:
   - Removed middle date portion from formats like 'Nov-03-21' → 'Nov-21'
   - Applied regex pattern matching to ensure 'Mon-YY' format

4. **Final Validation**:
   - **Correct format**: 36,391 entries
   - **Incorrect format**: 1,016 entries

**Action**: Dropped 1,016 rows that could not be transformed to the required format.

**Final Result**: 36,391 entries with standardized 'Mon-YY' format in months column.

---

## 5. Customer Column Cleaning

### 5.1 Initial State
- **Non-null entries**: 36,391 (after previous cleaning steps)
- **Unique customers**: 158 (before cleaning)

### 5.2 Date-like Value Removal
**Issue**: Some month values ('Jun-21', 'Jul-21', etc.) were present in the customer column.

**Action**: Replaced date-like values with 'Unspecified':
- Replaced: 'Jun-21', 'Jul-21', 'Aug-21', 'Sep-21', 'Oct-21', 'Nov-21', 'Dec-21', 'Jan-22', 'Feb-22', 'Mar-22'

### 5.3 Whitespace Cleaning
**Action**: Stripped leading and trailing spaces from all customer names.

### 5.4 Case Standardization
**Action**: Converted all customer names to lowercase for consistency.

**Result**: 150 unique customers (reduced from 158 due to case normalization and deduplication).

### 5.5 Data Recovery
**Action**: For customers marked as 'unspecified', checked if the date column contained non-numeric customer names and replaced 'unspecified' with the actual customer name from the date column.

**Result**: Improved data quality by recovering actual customer names that were misplaced.

---

## 6. Style Column Cleaning

### 6.1 Case Standardization
**Action**: Converted all style codes to lowercase.

### 6.2 Whitespace Cleaning
**Action**: Stripped leading and trailing whitespace from style codes.

### 6.3 Final State
- **Non-null entries**: 36,391
- **Unique styles**: 149 (after normalization)

**Note**: 1,037 style values were previously recovered from the date column during the date cleaning phase.

---

## 7. SKU Column Cleaning

### 7.1 Initial State
- **Non-null entries**: 34,957 (1,434 missing values)

### 7.2 Basic Cleaning
**Action**: 
- Converted SKU to string type
- Converted to lowercase
- Stripped whitespace

**Issue**: After conversion to string, NaN values became the string 'nan'.

### 7.3 Missing Value Imputation Strategy
**Problem**: 1,434 missing SKU values needed to be filled.

**Solution**: Created a helper column `skuuuu` by extracting the last segment after splitting SKU by '-'. This was used to help clean the size column and infer missing SKU values.

**Imputation Method**: For missing SKU values (string 'nan'), created SKU using format: `{style}-un-{size}`
- Where `un` stands for "unknown"
- Example: If style='abc123' and size='m', SKU becomes 'abc123-un-m'

**Result**: All SKU values filled, maintaining traceability of imputed values through the 'un' marker.

---

## 8. Size Column Cleaning

### 8.1 Initial State
- **Non-null entries**: 36,391
- **Unique sizes**: Multiple formats and inconsistencies

### 8.2 Size Standardization
**Actions**:
1. **Replaced extended sizes**: 
   - '5XL' → 'xxxxxl'
   - '6XL' → 'xxxxxxl'
   - '4XL' → 'xxxxl'

2. **Case standardization**: Converted all sizes to lowercase

3. **Numeric value correction**: 
   - Identified numeric values in size column (e.g., '1.00', '2.00', '1000.00')
   - Used the `skuuuu` helper column (extracted from SKU) to infer correct sizes
   - If `skuuuu` contained a valid size from allowed set, replaced numeric size with the correct size value
   - **Allowed sizes**: 'l', 'xl', 'xxl', 's', 'm', 'xs', 'xxxl', 's to xxl', 'free', 'xxxxxl', 'xxxxxxl', 'xxxxl'

**Result**: Standardized size values reduced from 20+ unique values to a consistent set of size categories.

---

## 9. Numeric Columns Cleaning

### 9.1 PCS (Pieces) Column
**Initial State**: Object type (string)

**Action**: Converted to `float64` data type.

**Result**: Proper numeric type for mathematical operations.

### 9.2 RATE Column
**Initial State**: Object type (string)

**Action**: Converted to `float64` data type.

**Result**: Proper numeric type for price calculations.

### 9.3 GROSS AMT (Gross Amount) Column
**Initial State**: Object type (string)

**Action**: Converted to `float64` data type.

**Result**: Proper numeric type for financial calculations.

---

## 10. Feature Engineering

### 10.1 Month Feature Creation
**Objective**: Extract structured month and year information from the 'Mon-YY' format.

**Process**:
- Extracted month abbreviation and year from `months` column
- Created `month` feature as a Period object (e.g., '2021-06', '2022-04')
- Format: Converted 'Jun-21' → '2021-06' (Period format)

**Result**: New `month` column with Period data type for time-based analysis.

### 10.2 Column Removal
**Columns Dropped**:
1. **`date`**: Contained non-date types that couldn't be reliably converted
2. **`months`**: Replaced by the new `month` feature
3. **`skuuuu`**: Temporary helper column, no longer needed

**Rationale**: Removed redundant or problematic columns while preserving essential information in better formats.

---

## 11. Final Dataset State

### 11.1 Final Statistics
- **Total Records**: 36,391 entries
- **Total Columns**: 8 columns
- **Data Types**: 
  - Object: 5 columns (customer, style, sku, size, month)
  - Float64: 3 columns (pcs, rate, gross_amt)
- **Memory Usage**: 2.8+ MB

### 11.2 Final Column Structure
1. `month` - Period type (YYYY-MM format)
2. `customer` - String (lowercase, 150 unique values)
3. `style` - String (lowercase, 149 unique values)
4. `sku` - String (lowercase, all values filled)
5. `size` - String (lowercase, standardized sizes)
6. `pcs` - Float64 (pieces/quantity)
7. `rate` - Float64 (price rate)
8. `gross_amt` - Float64 (gross amount)

### 11.3 Data Quality Improvements
- **Missing Values**: Eliminated (all columns now have 36,391 non-null entries)
- **Data Consistency**: Achieved through standardization (case, format, whitespace)
- **Data Recovery**: Recovered 1,037 style values and 2 customer values from misplaced data
- **Type Correctness**: All numeric columns properly typed as float64
- **Format Standardization**: All text columns lowercase, trimmed, and consistently formatted

---

## 12. Output Files Generated

### 12.1 Intermediate Cleaned Dataset
**File**: `data/IntlsalesReport_Cleaned.csv`
- Contains cleaned data with all imputations
- Includes temporary helper columns
- Ready for feature engineering

### 12.2 Final Cleaned Dataset
**File**: `data/IntlsalesReport_FinalCleaned.csv`
- Final production-ready dataset
- Feature-engineered with month column
- Removed temporary and redundant columns
- Optimized for machine learning and analysis

---

## 13. Key Challenges and Solutions

### Challenge 1: Misplaced Data
**Problem**: Customer names and style codes were in the date column.

**Solution**: Implemented intelligent data recovery by identifying patterns and relocating data to correct columns.

### Challenge 2: Inconsistent Date/Month Formats
**Problem**: Multiple date formats and incorrect month representations.

**Solution**: Created regex-based format detection and conversion functions to standardize all entries.

### Challenge 3: Missing SKU Values
**Problem**: 1,434 missing SKU values (3.9% of dataset).

**Solution**: Implemented rule-based imputation using style and size information, with clear markers ('un') to identify imputed values.

### Challenge 4: Numeric Values in Size Column
**Problem**: Size column contained numeric values instead of size codes.

**Solution**: Used SKU information to infer correct sizes and replace numeric values.

---

## 14. Data Quality Metrics

### Before Cleaning
- Missing values: ~1,040 rows (2.8%)
- Inconsistent formats: Multiple
- Data type issues: 3 numeric columns as strings
- Misplaced data: Present in date column

### After Cleaning
- Missing values: 0 (0%)
- Consistent formats: All standardized
- Data type issues: Resolved (all proper types)
- Misplaced data: Recovered and relocated

### Data Loss
- **Rows dropped**: 1,041 (2.8% of original dataset)
  - 1 row: Missing date
  - 24 rows: Missing months with no recoverable data
  - 1,016 rows: Months in non-transformable format

**Justification**: Dropped rows had insufficient or irrecoverable data that would have compromised analysis quality.

---

## 15. Recommendations for Future Use

1. **Data Validation**: Implement validation checks at data entry to prevent misplaced data
2. **Format Standards**: Establish clear format standards for dates, months, and sizes
3. **Missing Data Handling**: Consider implementing more sophisticated imputation methods if more SKU data becomes available
4. **Monitoring**: Track data quality metrics over time to identify patterns in data issues
5. **Documentation**: Maintain documentation of data cleaning steps for reproducibility

---

## 16. Conclusion

The data cleaning process successfully transformed a raw, inconsistent dataset into a clean, structured, and analysis-ready dataset. Through systematic cleaning, intelligent data recovery, and feature engineering, the dataset quality was significantly improved:

- **100% data completeness** (no missing values)
- **Consistent formatting** across all columns
- **Proper data types** for all columns
- **Recovered misplaced data** (1,039 values)
- **Feature engineering** for time-based analysis

The cleaned dataset is now ready for exploratory data analysis, machine learning model development, and business intelligence applications.

---

**Report Generated**: Based on analysis of `dataCleaning.ipynb`  
**Dataset**: Amazon Apparel Sales Dataset  
**Final Output**: `IntlsalesReport_FinalCleaned.csv`

