# Intermediate Python - Week 1

## Python setup:

### 🐞 Fix the VS Code Shell Issue + Upgrade Python version with `pyenv`
- There was an error starting the terminal. I saw this printed in my terminal every terminal window that was opened:
```bash
pyenv shell 3.8.16
USER course-python-4-production % pyenv shell 3.8.16
pyenv: shell integration not enabled. Run `pyenv init' for instructions.
```

- I tried to run `pyenv init`, which printed out the following in the terminal:
```bash
# Load pyenv automatically by appending
# the following to 
~/.zprofile (for login shells)
and ~/.zshrc (for interactive shells) :

export PYENV_ROOT="$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

# Restart your shell for the changes to take effect.
```

But this didn't fix it because the python version was still `3.8.16` when I'd open a new terminal window in VS Code.

So what I had to do was run this to get Python 3.10.8 installed locally using pyenv because I did not have this version of Python installed locally, as is required in the main README.md file in the root of this repository:
```bash
pyenv install 3.10.8
```

Then I set Python 3.10.8 as the local version for the project:
```bash
pyenv local 3.10.8
```

I saw that this created a `.python-version` file in the root of the repo that lists this specified version of Python:
```txt
3.10.8
```

I also ran this command to set the version of Python as 3.10.8 globally for my system:
```bash
pyenv global 3.10.8
```

However, after all of the above, VS Code was still logging those 3 lines with the outdated version of Python as above, `pyenv shell 3.8.16`, so I found this GitHub issue on the [Microsoft/vscode-python](https://github.com/Microsoft/vscode-python/issues/3066) page that talked about disabling this action in VSCode: `"python.terminal.activateEnvironment": "false"`

I found in the VS Code settings under `pyenv` in search, you can uncheck this box:

```bash
Python › Terminal: Activate Environment
[ ] Activate Python Environment in all Terminals created.
```

✅ New terminal windows now don't try to run the old python version!


### 🐞 `pip` isn't recognized, but `pip3` is

- Change directory into the `.zshrc` file and Vim into it so we can add an alias
```
vim ~/.zshrc
```

- In this file I see the following:
```bash
alias python=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3

export PATH="$PATH:/Users/.../Development/flutter/bin"
...
```

- I added the alias script, `alias pip=pip3`, on the 2nd line:
```bash
alias python=/Library/Frameworks/Python.framework/Versions/3.11/bin/python3
alias pip=pip3
export PATH="$PATH:/Users/.../Development/flutter/bin"
...
```

- Then I pressed [ESC], typed `:wq` and then pressed [ENTER] (meaning with saving, quit, in Vim)

- Test this by running:
    - If this works, this should print something like : `pip 23.0.1 from /Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/site-packages/pip (python 3.11)`
```bash
pip --version
```



# Install the modules:

Run:
```bash
pip install -r requirements.txt
```

I was prompted to upgrade pip3, so I did that with this command:
```bash
pip3 install --upgrade pip
```



# Generate 3 datasets:

These datasets are then processed into the `data` directory: `/data/xyz`

```bash
# Generate test data (useful for unit testing code)
python generate_data.py --type tst
```

```bash
# Generate sml data (useful for quick testing of logic)
python generate_data.py --type sml
```

```bash
# Generate the real data data (actual data)
python generate_data.py --type bg
```


```bash
.
├── data
│   ├── bg
│   ├── seed
│   ├── sml
│   └── tst
```

# Build a data processing module

## Part 1: Update the `aggregrate()` method in the `utils.py` file, so that it uses the generator method assigned to `self.data_reader` and returns the aggregate of the column mentioned in the `column_name` variable.

This took a bit of time to understand what was required here, but basically, I needed to create a `generator()` function with the `yield` keyword to go one by one over each row of the `.csv` file and then turn it into a dictionary in the following format:
```json
{'StockCode': '22180','Description': 'RETROSPOT LAMP','UnitPrice': 19.96,'Quantity': 4,'TotalPrice': 79.84,'Country': 'Russia',}
```


Here are some examples of the outputs to show that it worked:
```json
{'StockCode': '21270', 'Description': 'ANTIQUE CREAM CUTLERY CUPBOARD', 'UnitPrice': '12.75', 'Quantity': '1', 'TotalPrice': '12.75', 'Country': 'Canada'}
{'StockCode': '84859A', 'Description': 'SILVER DISCO HANDBAG', 'UnitPrice': '4.13', 'Quantity': '1', 'TotalPrice': '4.13', 'Country': 'United Kingdom'}
{'StockCode': '22183', 'Description': 'CAKE STAND VICTORIAN FILIGREE MED', 'UnitPrice': '6.75', 'Quantity': '3', 'TotalPrice': '20.25', 'Country': 'Russia'}
{'StockCode': '20694', 'Description': 'FLORAL PINK MONSTER', 'UnitPrice': '7.46', 'Quantity': '4', 'TotalPrice': '29.84', 'Country': 'United States'}
```

## Part 2: Update the `aggregrate()` method in the `data_processor.py` file, so that it uses the generator method assigned to `self.data_reader` and returns the aggregate of the column mentioned in the `column_name` variable.

### 🐞 Issue running the script: `No module named 'w1'`

Everytime I ran `python data_processor.py`, I would get this error:
```bash
Traceback (most recent call last):
  File "/Users/.../.../.../.../.../course-python-4-production/w1/data_processor.py", line 3, in <module>
    from w1.utils import Stats, DataReader
ModuleNotFoundError: No module named 'w1'
```

This was strange because I did not understand about the relative imports of w1.utils. So what I did was change this line of code:
`from w1.utils import Stats, DataReader`
to this:
`from utils import Stats, DataReader`

Then once I cd'ed into the `w1` directory, I could execute the `data_processor.py` file by executing `python data_processor.py` 

### Round the aggregate value to 2 decimals:

Because of the long float values in the CSV for many of the TotalPrice values, I ran my script and got this as an output:
```bash
90000it [00:00, 1113016.57it/s]

Statistics for the specified columns:
90000it [00:00, 716452.50it/s]
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 34.022147577775236,
 'median': None,
 'min': 0.001,
 'std': 1215.827969633452}
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.192059144442679,
 'median': None,
 'min': 0.001,
 'std': 305.12369162688367}
90000it [00:00, 925098.48it/s]

Aggregate for TotalPrice: 3061993.281999771
```

What I want to do is return this value: `3061993.28`, not `3061993.281999771`

To do this, I figured it would be more efficient to aggregate all the `TotalPrice` values and THEN round, so that is what I implemented with the round method here:
`total_price_aggregate = round(processor.aggregate('TotalPrice'), 2)`

This then allowed me to get the following output:
```bash
90000it [00:00, 1095611.20it/s]

Statistics for the specified columns:
90000it [00:00, 737389.46it/s]
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 34.022147577775236,
 'median': None,
 'min': 0.001,
 'std': 1215.827969633452}
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.192059144442679,
 'median': None,
 'min': 0.001,
 'std': 305.12369162688367}
90000it [00:00, 906582.51it/s]

Aggregate for TotalPrice: 3061993.28
```


### Fix the outputs to only log the Aggregate of TotalPrice:

To remove the statistics from logging out, I simply commented out them in the execution script.

This then brought the output to this:
```bash
90000it [00:00, 1118580.50it/s]
90000it [00:00, 948289.15it/s]

Aggregate for TotalPrice: 3061993.28
```

To get rid of those first 2 lines, I needed to adjust the `tqdm` lines from this:
`for row in tqdm(data_reader_gen):`
to this:
`for row in data_reader_gen:`

This allowed the output to then be this:
```bash
Aggregate for TotalPrice: 3061993.28
```


## Part 3: Update the `revenue_per_region()` method in the `main.py` file, so that it takes an object of instance type `DataProcessor` as an input, and returns a dictionary containing country names as keys and the revenue recorded for that country as values.

### 🐞 Issue running function: `constants not found`

I needed to change the import of the `constants.py` file as I was running the file from within `w1`. This was the error I received:
```bash
Traceback (most recent call last):
  File "/Users/.../.../.../.../.../course-python-4-production/w1/main.py", line 1, in <module>
    import constants
ModuleNotFoundError: No module named 'constants'
```
To fix this, I needed to change this line:
`import constants`
to this:
```py
import sys
# Adds the parent directory to the system path for this execution.
sys.path.append("..") 
import constants
```

This works because we are progrmmatically adjusting the path to include the parent directory (where `constants.py` lives in the root directory of the project) so that our `main.py` file in the `w1` directory can run.

By adding the `sys.path.append("..")` line, this means we are adding the parent directory of the script to the list of directories, so that Python will now look in that directory for any modules we're trying to import.


### Fine-tune the output to model what the requirement is:
When the output printed, I saw the progress output from `tqdm` and other data points as well:
```bash
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 11.291125247057265,
 'median': None,
 'min': 0.001,
 'std': 326.33789059131743}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 15.0,
 'max': 178364.59999999998,
 'mean': 40.535017341173344,
 'median': None,
 'min': 0.001,
 'std': 1450.293352932578}
85000it [00:00, 865405.33it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.192059144442679,
 'median': None,
 'min': 0.001,
 'std': 305.12369162688367}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 34.022147577775236,
 'median': None,
 'min': 0.001,
 'std': 1215.827969633452}
90000it [00:00, 905241.13it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.251292749998372,
 'median': None,
 'min': 0.001,
 'std': 304.7065793845803}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 14.95,
 'max': 160528.13999999998,
 'mean': 33.799728674996885,
 'median': None,
 'min': 0.001,
 'std': 1190.5829118072277}
80000it [00:00, 921607.31it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 11.330868586665728,
 'median': None,
 'min': 0.001,
 'std': 334.1514598566704}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 14.92,
 'max': 160528.13999999998,
 'mean': 38.06841777332996,
 'median': None,
 'min': 0.001,
 'std': 1373.0997878996477}
75000it [00:00, 893198.22it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.996214966667246,
 'median': None,
 'min': 0.001,
 'std': 327.7099314175273}
'TotalPrice'
{'25': 2.55,
 '50': 6.6,
 '75': 14.92,
 'max': 142691.68,
 'mean': 37.75857793332999,
 'median': None,
 'min': 0.001,
 'std': 1300.1082879602784}
60000it [00:00, 917569.95it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 10.211510830769738,
 'median': None,
 'min': 0.001,
 'std': 314.13738240948175}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.96,
 'max': 142691.68,
 'mean': 33.573793953841665,
 'median': None,
 'min': 0.001,
 'std': 1193.563308179154}
65000it [00:00, 912446.07it/s]
'UnitPrice'
{'25': 1.25,
 '50': 2.46,
 '75': 4.95,
 'max': 17836.46,
 'mean': 8.994602442857856,
 'median': None,
 'min': 0.001,
 'std': 271.6167592177564}
'TotalPrice'
{'25': 2.55,
 '50': 6.58,
 '75': 14.940000000000001,
 'max': 142691.68,
 'mean': 29.73535868571067,
 'median': None,
 'min': 0.001,
 'std': 1031.4268413150558}
70000it [00:00, 889299.32it/s]
[{'file_name': '2020',
  'revenue_per_region': {'Canada': 256483.4730000059,
                         'China': 74456.44599999976,
                         'France': 514517.08100000897,
                         'Germany': 237569.51600000478,
                         'India': 285588.9710000039,
                         'Italy': 119300.93499999992,
                         'Japan': 143333.8180000012,
                         'Russia': 151637.39000000103,
                         'United Kingdom': 857584.4650000089,
                         'United States': 805067.7790000127}},
 {'file_name': '2021',
  'revenue_per_region': {'Canada': 224470.32800000274,
                         'China': 178848.89299999972,
                         'France': 573350.3030000051,
                         'Germany': 310229.4460000097,
                         'India': 372654.8150000077,
                         'Italy': 118160.19199999984,
                         'Japan': 160613.09300000157,
                         'Russia': 133403.88599999968,
                         'United Kingdom': 452914.8350000163,
                         'United States': 537491.9110000153}},
 {'file_name': '2019',
  'revenue_per_region': {'Canada': 175189.75200000269,
                         'China': 55700.899999999696,
                         'France': 163830.84700000272,
                         'Germany': 344796.47700000415,
                         'India': 219384.15700000426,
                         'Italy': 100704.47999999946,
                         'Japan': 104516.70399999959,
                         'Russia': 128384.35799999995,
                         'United Kingdom': 713114.2820000106,
                         'United States': 698518.9570000046}},
 {'file_name': '2018',
  'revenue_per_region': {'Canada': 287613.4960000032,
                         'China': 58399.010999999984,
                         'France': 188814.7070000001,
                         'Germany': 253322.9330000033,
                         'India': 287517.52600000676,
                         'Italy': 392249.87000000174,
                         'Japan': 417965.6910000028,
                         'Russia': 87128.37999999964,
                         'United Kingdom': 441791.4290000169,
                         'United States': 440634.24000001576}},
 {'file_name': '2015',
  'revenue_per_region': {'Canada': 247536.2030000024,
                         'China': 51776.66399999985,
                         'France': 119374.75100000021,
                         'Germany': 204787.72300000163,
                         'India': 201634.9490000025,
                         'Italy': 67570.03399999991,
                         'Japan': 44342.27699999988,
                         'Russia': 60174.84899999968,
                         'United Kingdom': 685184.4670000093,
                         'United States': 583205.5590000105}},
 {'file_name': '2016',
  'revenue_per_region': {'Canada': 207380.6540000017,
                         'China': 169976.69000000242,
                         'France': 174299.7430000016,
                         'Germany': 228624.89300000184,
                         'India': 97028.18399999924,
                         'Italy': 138279.71300000025,
                         'Japan': 71647.03999999979,
                         'Russia': 45856.22699999985,
                         'United Kingdom': 630329.2500000136,
                         'United States': 419100.81300001545}},
 {'file_name': '2017',
  'revenue_per_region': {'Canada': 130649.83999999946,
                         'China': 265664.7900000029,
                         'France': 237454.22700000252,
                         'Germany': 184079.89300000225,
                         'India': 112647.72499999957,
                         'Italy': 57028.194999999825,
                         'Japan': 195565.1490000015,
                         'Russia': 109447.99199999988,
                         'United Kingdom': 332960.15800000774,
                         'United States': 456056.6990000164}}]
```

To remove the `tqdm` progress, I removed the `tqdm()` wrapper around the for loop and any reference to tqdm in the script. This then allowed me to log this as the output, which is great because it also separates the files by filename so I can see the outputs like this:
```bash
[{'file_name': '2020',
  'revenue_per_region': {'Canada': 256483.4730000059,
                         'China': 74456.44599999976,
                         'France': 514517.08100000897,
                         'Germany': 237569.51600000478,
                         'India': 285588.9710000039,
                         'Italy': 119300.93499999992,
                         'Japan': 143333.8180000012,
                         'Russia': 151637.39000000103,
                         'United Kingdom': 857584.4650000089,
                         'United States': 805067.7790000127}},
 {'file_name': '2021',
  'revenue_per_region': {'Canada': 224470.32800000274,
                         'China': 178848.89299999972,
                         'France': 573350.3030000051,
                         'Germany': 310229.4460000097,
                         'India': 372654.8150000077,
                         'Italy': 118160.19199999984,
                         'Japan': 160613.09300000157,
                         'Russia': 133403.88599999968,
                         'United Kingdom': 452914.8350000163,
                         'United States': 537491.9110000153}},
 {'file_name': '2019',
  'revenue_per_region': {'Canada': 175189.75200000269,
                         'China': 55700.899999999696,
                         'France': 163830.84700000272,
                         'Germany': 344796.47700000415,
                         'India': 219384.15700000426,
                         'Italy': 100704.47999999946,
                         'Japan': 104516.70399999959,
                         'Russia': 128384.35799999995,
                         'United Kingdom': 713114.2820000106,
                         'United States': 698518.9570000046}},
 {'file_name': '2018',
  'revenue_per_region': {'Canada': 287613.4960000032,
                         'China': 58399.010999999984,
                         'France': 188814.7070000001,
                         'Germany': 253322.9330000033,
                         'India': 287517.52600000676,
                         'Italy': 392249.87000000174,
                         'Japan': 417965.6910000028,
                         'Russia': 87128.37999999964,
                         'United Kingdom': 441791.4290000169,
                         'United States': 440634.24000001576}},
 {'file_name': '2015',
  'revenue_per_region': {'Canada': 247536.2030000024,
                         'China': 51776.66399999985,
                         'France': 119374.75100000021,
                         'Germany': 204787.72300000163,
                         'India': 201634.9490000025,
                         'Italy': 67570.03399999991,
                         'Japan': 44342.27699999988,
                         'Russia': 60174.84899999968,
                         'United Kingdom': 685184.4670000093,
                         'United States': 583205.5590000105}},
 {'file_name': '2016',
  'revenue_per_region': {'Canada': 207380.6540000017,
                         'China': 169976.69000000242,
                         'France': 174299.7430000016,
                         'Germany': 228624.89300000184,
                         'India': 97028.18399999924,
                         'Italy': 138279.71300000025,
                         'Japan': 71647.03999999979,
                         'Russia': 45856.22699999985,
                         'United Kingdom': 630329.2500000136,
                         'United States': 419100.81300001545}},
 {'file_name': '2017',
  'revenue_per_region': {'Canada': 130649.83999999946,
                         'China': 265664.7900000029,
                         'France': 237454.22700000252,
                         'Germany': 184079.89300000225,
                         'India': 112647.72499999957,
                         'Italy': 57028.194999999825,
                         'Japan': 195565.1490000015,
                         'Russia': 109447.99199999988,
                         'United Kingdom': 332960.15800000774,
                         'United States': 456056.6990000164}}]
```

### How to select the right file(s) to look at:

By default, if you don't specify the directory, the script will automatically pick all of the data in the `tst` directory when you run:

```bash
python main.py
```

^ See the output above.


This is defined in this part of the Python script:
```py
parser = argparse.ArgumentParser(description="Choose from one of these : [tst|sml|bg]")
parser.add_argument('--type',
                    default='tst',
                    choices=['tst', 'sml', 'bg'],
                    help='Type of data to generate')
args = parser.parse_args()
```

So when you specify a file flag, like this:
```bash
python main.py --type=sml
```

It will print out different outputs than `tst`, because we specified we wanted the datasets in the `sml` folder:
```bash
[{'file_name': '2020',
  'revenue_per_region': {'Canada': 2937322.762999638,
                         'China': 1281620.1119999199,
                         'France': 3100884.353999692,
                         'Germany': 2924484.6949997055,
                         'India': 3393255.1319997488,
                         'Italy': 1395093.5609999371,
                         'Japan': 1180115.229999936,
                         'Russia': 1889921.5339998663,
                         'United Kingdom': 6572918.120999353,
                         'United States': 5957026.824999307}},
 {'file_name': '2021',
  'revenue_per_region': {'Canada': 2943469.3109996556,
                         'China': 1593765.8999998556,
                         'France': 3021699.904999693,
                         'Germany': 3315395.8949997425,
                         'India': 2687389.5299995956,
                         'Italy': 1527126.7059998394,
                         'Japan': 1845020.4799998796,
                         'Russia': 1669360.814999858,
                         'United Kingdom': 6291216.839999231,
                         'United States': 7235611.156999284}},
 {'file_name': '2019',
  'revenue_per_region': {'Canada': 2879380.837999795,
                         'China': 1191279.6719999942,
                         'France': 2535158.5059996555,
                         'Germany': 2848414.7829997884,
                         'India': 3624641.5619997196,
                         'Italy': 1592184.9569999324,
                         'Japan': 1198325.4299999862,
                         'Russia': 1236670.3449999923,
                         'United Kingdom': 4424134.155999426,
                         'United States': 5577276.419999438}},
 {'file_name': '2018',
  'revenue_per_region': {'Canada': 3215835.6049996773,
                         'China': 1168869.5219999678,
                         'France': 3231369.3649997357,
                         'Germany': 2394873.3069997584,
                         'India': 2932711.2069997033,
                         'Italy': 1199493.7549999717,
                         'Japan': 1034675.2490000221,
                         'Russia': 970693.6860000177,
                         'United Kingdom': 4776333.160999374,
                         'United States': 4870173.898999412}},
 {'file_name': '2015',
  'revenue_per_region': {'Canada': 1720671.8619998104,
                         'China': 912291.2940000148,
                         'France': 2213877.21099984,
                         'Germany': 1999042.04799976,
                         'India': 1692236.4009998492,
                         'Italy': 1104618.8150000083,
                         'Japan': 1271401.4039999626,
                         'Russia': 771317.1550000184,
                         'United Kingdom': 4410573.975999488,
                         'United States': 4587794.878999568}},
 {'file_name': '2016',
  'revenue_per_region': {'Canada': 1780207.161999797,
                         'China': 909033.9610000108,
                         'France': 1933642.3199996992,
                         'Germany': 2084211.4269997417,
                         'India': 3028964.6689997134,
                         'Italy': 1099943.5199999951,
                         'Japan': 1317518.8339999532,
                         'Russia': 1405669.4139999116,
                         'United Kingdom': 3769398.9839995746,
                         'United States': 4164833.920999495}},
 {'file_name': '2017',
  'revenue_per_region': {'Canada': 2136029.573999653,
                         'China': 850915.679000018,
                         'France': 2410945.473999692,
                         'Germany': 2633481.8979996997,
                         'India': 2179182.235999732,
                         'Italy': 1241122.9089999504,
                         'Japan': 1023822.4930000178,
                         'Russia': 1623738.41799995,
                         'United Kingdom': 5213959.188999466,
                         'United States': 3689693.8239994845}}]
```

Wooo! It works 🥳

# 🧪 Testing in Python with `pytest`

## Make sure pytest is installed if it isn't already:
```
pip install pytest
```

## Run tests with prints
- The `PYTHONPATH=../` part is to make sure that when `pytest` runs, the program knows where to look for the modules you're importing in the script. 
- The `-s` flag allows any print statement in yoru code to show in the temrinal.

```
PYTHONPATH=../ pytest test.py -s
```

This was the output I received:
```bash
==================================================== test session starts ====================================================
platform darwin -- Python 3.11.3, pytest-7.2.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w1
plugins: anyio-4.0.0
collected 2 items                                                                                                           

test.py {'Country': 'France',
 'Date': '2015/04/06',
 'Description': 'HEART BUTTONS JEWELLERY BOX',
 'InvoiceNo': 'f1bce1a2-5032-11ee-826f-2e9565c92f30',
 'Quantity': '1',
 'StockCode': '82095',
 'TotalPrice': '4.96',
 'UnitPrice': '4.96'}
.[{'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2020.csv',
  'revenue_data': {'file_name': '2020',
                   'revenue_per_region': {'Canada': 256483.4730000059,
                                          'China': 74456.44599999976,
                                          'France': 514517.08100000897,
                                          'Germany': 237569.51600000478,
                                          'India': 285588.9710000039,
                                          'Italy': 119300.93499999992,
                                          'Japan': 143333.8180000012,
                                          'Russia': 151637.39000000103,
                                          'United Kingdom': 857584.4650000089,
                                          'United States': 805067.7790000127}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2021.csv',
  'revenue_data': {'file_name': '2021',
                   'revenue_per_region': {'Canada': 224470.32800000274,
                                          'China': 178848.89299999972,
                                          'France': 573350.3030000051,
                                          'Germany': 310229.4460000097,
                                          'India': 372654.8150000077,
                                          'Italy': 118160.19199999984,
                                          'Japan': 160613.09300000157,
                                          'Russia': 133403.88599999968,
                                          'United Kingdom': 452914.8350000163,
                                          'United States': 537491.9110000153}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2019.csv',
  'revenue_data': {'file_name': '2019',
                   'revenue_per_region': {'Canada': 175189.75200000269,
                                          'China': 55700.899999999696,
                                          'France': 163830.84700000272,
                                          'Germany': 344796.47700000415,
                                          'India': 219384.15700000426,
                                          'Italy': 100704.47999999946,
                                          'Japan': 104516.70399999959,
                                          'Russia': 128384.35799999995,
                                          'United Kingdom': 713114.2820000106,
                                          'United States': 698518.9570000046}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2018.csv',
  'revenue_data': {'file_name': '2018',
                   'revenue_per_region': {'Canada': 287613.4960000032,
                                          'China': 58399.010999999984,
                                          'France': 188814.7070000001,
                                          'Germany': 253322.9330000033,
                                          'India': 287517.52600000676,
                                          'Italy': 392249.87000000174,
                                          'Japan': 417965.6910000028,
                                          'Russia': 87128.37999999964,
                                          'United Kingdom': 441791.4290000169,
                                          'United States': 440634.24000001576}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2015.csv',
  'revenue_data': {'file_name': '2015',
                   'revenue_per_region': {'Canada': 247536.2030000024,
                                          'China': 51776.66399999985,
                                          'France': 119374.75100000021,
                                          'Germany': 204787.72300000163,
                                          'India': 201634.9490000025,
                                          'Italy': 67570.03399999991,
                                          'Japan': 44342.27699999988,
                                          'Russia': 60174.84899999968,
                                          'United Kingdom': 685184.4670000093,
                                          'United States': 583205.5590000105}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2016.csv',
  'revenue_data': {'file_name': '2016',
                   'revenue_per_region': {'Canada': 207380.6540000017,
                                          'China': 169976.69000000242,
                                          'France': 174299.7430000016,
                                          'Germany': 228624.89300000184,
                                          'India': 97028.18399999924,
                                          'Italy': 138279.71300000025,
                                          'Japan': 71647.03999999979,
                                          'Russia': 45856.22699999985,
                                          'United Kingdom': 630329.2500000136,
                                          'United States': 419100.81300001545}}},
 {'file_path': '/.../.../.../.../.../.../course-python-4-production/w1/../data/tst/2017.csv',
  'revenue_data': {'file_name': '2017',
                   'revenue_per_region': {'Canada': 130649.83999999946,
                                          'China': 265664.7900000029,
                                          'France': 237454.22700000252,
                                          'Germany': 184079.89300000225,
                                          'India': 112647.72499999957,
                                          'Italy': 57028.194999999825,
                                          'Japan': 195565.1490000015,
                                          'Russia': 109447.99199999988,
                                          'United Kingdom': 332960.15800000774,
                                          'United States': 456056.6990000164}}}]
.

===================================================== 2 passed in 1.37s =====================================================
```

## Run tests without prints 
```
PYTHONPATH=../ pytest test.py
```

This logged as the output:
```bash
==================================================== test session starts ====================================================
platform darwin -- Python 3.11.3, pytest-7.2.2, pluggy-1.3.0
rootdir: /Users/.../.../.../.../.../course-python-4-production/w1
plugins: anyio-4.0.0
collected 2 items                                                                                                           

test.py ..                                                                                                            [100%]

===================================================== 2 passed in 1.41s =====================================================
```

# Run the code
Now that we've tested our code and both tests pass successfully, we can now start testing our code on the datasets we have.

````
# Run on `test` data
PYTHONPATH=../ python main.py --type tst

# Run on `small` data
PYTHONPATH=../ python main.py --type sml

# Run on the `big` data
PYTHONPATH=../ python main.py --type bg
````

Running these commands generated corresponding file outputs in the `/output` folder which also inside of each folder dropped in corresponding `.json` files and `.png` bar charts of the data.

Phew, this was a lot! 😅