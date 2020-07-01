title: "Using sklearn Pipelines and Voting Classifier"
details: "Using sklearn Pipelines and Voting Classifiers for Kaggle's Titanic Challenge"
date: 2020-04-04
lastmod: 2020-04-05

<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Table-of-Contents">Table of Contents<a class="anchor-link" href="#Table-of-Contents">&#182;</a></h2><ol>
<li><a href="#data-extraction">Date Extraction</a></li>
<li><a href="#data-investigation">Data Investigation</a></li>
<li><a href="#feature-selection">Feature Selection</a></li>
<li><a href="#imports">General Imports</a></li>
<li><a href="#pipeline">Preprocessing Pipeline</a></li>
<li><a href="#models">Models</a><ul>
<li><a href="#lr">Logistic Regression</a></li>
<li><a href="#rf">Random Forest</a></li>
<li><a href="#svc">SVC</a></li>
<li><a href="#mlp">MLP</a></li>
<li><a href="#vc">Voting Classifier</a></li>
</ul>
</li>
</ol>

</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Data-Extraction-">Data Extraction <a class="anchor" id="data-extraction" /><a class="anchor-link" href="#Data-Extraction-">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[23]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">warnings</span>
<span class="n">warnings</span><span class="o">.</span><span class="n">filterwarnings</span><span class="p">(</span><span class="s1">&#39;ignore&#39;</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[16]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="kn">import</span> <span class="nn">pandas</span> <span class="k">as</span> <span class="nn">pd</span>
<span class="kn">from</span> <span class="nn">mlxtend.plotting</span> <span class="kn">import</span> <span class="n">plot_decision_regions</span>

<span class="kn">import</span> <span class="nn">os</span>
<span class="kn">from</span> <span class="nn">pprint</span> <span class="kn">import</span> <span class="n">pprint</span>

<span class="n">dfs</span> <span class="o">=</span> <span class="p">[]</span>
<span class="k">for</span> <span class="n">dirname</span><span class="p">,</span> <span class="n">_</span><span class="p">,</span> <span class="n">filenames</span> <span class="ow">in</span> <span class="n">os</span><span class="o">.</span><span class="n">walk</span><span class="p">(</span><span class="s1">&#39;.&#39;</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">filename</span> <span class="ow">in</span> <span class="n">filenames</span><span class="p">:</span>
        <span class="k">if</span><span class="p">(</span><span class="n">filename</span> <span class="ow">in</span> <span class="p">{</span><span class="s1">&#39;train.csv&#39;</span><span class="p">,</span> <span class="s1">&#39;test.csv&#39;</span><span class="p">}):</span>
            <span class="n">dfs</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">pd</span><span class="o">.</span><span class="n">read_csv</span><span class="p">(</span><span class="n">os</span><span class="o">.</span><span class="n">path</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">dirname</span><span class="p">,</span> <span class="n">filename</span><span class="p">)))</span>

<span class="n">test</span><span class="p">,</span> <span class="n">train</span> <span class="o">=</span> <span class="n">dfs</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Data-Investigation-">Data Investigation <a class="anchor" id="data-investigation" /><a class="anchor-link" href="#Data-Investigation-">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[7]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">train</span><span class="o">.</span><span class="n">isnull</span><span class="p">()</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt output_prompt">Out[7]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>PassengerId      0
Survived         0
Pclass           0
Name             0
Sex              0
Age            177
SibSp            0
Parch            0
Ticket           0
Fare             0
Cabin          687
Embarked         2
dtype: int64</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[8]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">train</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt output_prompt">Out[8]:</div>



<div class="output_html rendered_html output_subarea output_execute_result">
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>PassengerId</th>
      <th>Survived</th>
      <th>Pclass</th>
      <th>Name</th>
      <th>Sex</th>
      <th>Age</th>
      <th>SibSp</th>
      <th>Parch</th>
      <th>Ticket</th>
      <th>Fare</th>
      <th>Cabin</th>
      <th>Embarked</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>3</td>
      <td>Braund, Mr. Owen Harris</td>
      <td>male</td>
      <td>22.0</td>
      <td>1</td>
      <td>0</td>
      <td>A/5 21171</td>
      <td>7.2500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>1</td>
      <td>1</td>
      <td>Cumings, Mrs. John Bradley (Florence Briggs Th...</td>
      <td>female</td>
      <td>38.0</td>
      <td>1</td>
      <td>0</td>
      <td>PC 17599</td>
      <td>71.2833</td>
      <td>C85</td>
      <td>C</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3</td>
      <td>1</td>
      <td>3</td>
      <td>Heikkinen, Miss. Laina</td>
      <td>female</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>STON/O2. 3101282</td>
      <td>7.9250</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>3</th>
      <td>4</td>
      <td>1</td>
      <td>1</td>
      <td>Futrelle, Mrs. Jacques Heath (Lily May Peel)</td>
      <td>female</td>
      <td>35.0</td>
      <td>1</td>
      <td>0</td>
      <td>113803</td>
      <td>53.1000</td>
      <td>C123</td>
      <td>S</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>0</td>
      <td>3</td>
      <td>Allen, Mr. William Henry</td>
      <td>male</td>
      <td>35.0</td>
      <td>0</td>
      <td>0</td>
      <td>373450</td>
      <td>8.0500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>886</th>
      <td>887</td>
      <td>0</td>
      <td>2</td>
      <td>Montvila, Rev. Juozas</td>
      <td>male</td>
      <td>27.0</td>
      <td>0</td>
      <td>0</td>
      <td>211536</td>
      <td>13.0000</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>887</th>
      <td>888</td>
      <td>1</td>
      <td>1</td>
      <td>Graham, Miss. Margaret Edith</td>
      <td>female</td>
      <td>19.0</td>
      <td>0</td>
      <td>0</td>
      <td>112053</td>
      <td>30.0000</td>
      <td>B42</td>
      <td>S</td>
    </tr>
    <tr>
      <th>888</th>
      <td>889</td>
      <td>0</td>
      <td>3</td>
      <td>Johnston, Miss. Catherine Helen "Carrie"</td>
      <td>female</td>
      <td>NaN</td>
      <td>1</td>
      <td>2</td>
      <td>W./C. 6607</td>
      <td>23.4500</td>
      <td>NaN</td>
      <td>S</td>
    </tr>
    <tr>
      <th>889</th>
      <td>890</td>
      <td>1</td>
      <td>1</td>
      <td>Behr, Mr. Karl Howell</td>
      <td>male</td>
      <td>26.0</td>
      <td>0</td>
      <td>0</td>
      <td>111369</td>
      <td>30.0000</td>
      <td>C148</td>
      <td>C</td>
    </tr>
    <tr>
      <th>890</th>
      <td>891</td>
      <td>0</td>
      <td>3</td>
      <td>Dooley, Mr. Patrick</td>
      <td>male</td>
      <td>32.0</td>
      <td>0</td>
      <td>0</td>
      <td>370376</td>
      <td>7.7500</td>
      <td>NaN</td>
      <td>Q</td>
    </tr>
  </tbody>
</table>
<p>891 rows × 12 columns</p>
</div>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Feature-Selection-">Feature Selection <a class="anchor" id="feature-selection" /><a class="anchor-link" href="#Feature-Selection-">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[9]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">X</span> <span class="o">=</span> <span class="n">train</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Survived&#39;</span><span class="p">,</span> <span class="s1">&#39;Ticket&#39;</span><span class="p">,</span> <span class="s1">&#39;Name&#39;</span><span class="p">])</span>
<span class="n">y</span> <span class="o">=</span> <span class="n">train</span><span class="o">.</span><span class="n">loc</span><span class="p">[:,</span> <span class="p">[</span><span class="s1">&#39;Survived&#39;</span><span class="p">]]</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="General-imports-">General imports <a class="anchor" id="imports" /><a class="anchor-link" href="#General-imports-">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[25]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.model_selection</span> <span class="kn">import</span> <span class="n">GridSearchCV</span><span class="p">,</span><span class="n">RandomizedSearchCV</span>
<span class="kn">from</span> <span class="nn">sklearn.metrics</span> <span class="kn">import</span> <span class="n">accuracy_score</span>

<span class="kn">import</span> <span class="nn">joblib</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Preprocessing-Pipeline-">Preprocessing Pipeline <a class="anchor" id="pipeline" /><a class="anchor-link" href="#Preprocessing-Pipeline-">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[11]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.preprocessing</span> <span class="kn">import</span> <span class="n">StandardScaler</span>
<span class="kn">from</span> <span class="nn">sklearn.preprocessing</span> <span class="kn">import</span> <span class="n">PolynomialFeatures</span><span class="p">,</span> <span class="n">OneHotEncoder</span>
<span class="kn">from</span> <span class="nn">sklearn.impute</span> <span class="kn">import</span> <span class="n">SimpleImputer</span><span class="p">,</span> <span class="n">KNNImputer</span>

<span class="kn">from</span> <span class="nn">sklearn.pipeline</span> <span class="kn">import</span> <span class="n">Pipeline</span>
<span class="kn">from</span> <span class="nn">sklearn.compose</span> <span class="kn">import</span> <span class="n">ColumnTransformer</span>

<span class="n">numeric_features</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;Age&#39;</span><span class="p">,</span> <span class="s1">&#39;Fare&#39;</span><span class="p">]</span>

<span class="n">numeric_transformer</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[</span>
    <span class="p">(</span><span class="s1">&#39;imputer&#39;</span><span class="p">,</span> <span class="n">KNNImputer</span><span class="p">()),</span>
    <span class="p">(</span><span class="s1">&#39;scaler&#39;</span><span class="p">,</span> <span class="n">StandardScaler</span><span class="p">()),</span>
<span class="p">])</span> 

<span class="n">categorical_features</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;Embarked&#39;</span><span class="p">,</span> <span class="s1">&#39;Sex&#39;</span><span class="p">,</span> <span class="s1">&#39;Pclass&#39;</span><span class="p">,</span> <span class="s1">&#39;SibSp&#39;</span><span class="p">,</span> <span class="s1">&#39;Parch&#39;</span><span class="p">,</span> <span class="s1">&#39;Cabin&#39;</span><span class="p">]</span>
<span class="n">categorical_transformer</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[</span>
    <span class="p">(</span><span class="s1">&#39;imputer&#39;</span><span class="p">,</span> <span class="n">SimpleImputer</span><span class="p">(</span><span class="n">strategy</span><span class="o">=</span><span class="s1">&#39;constant&#39;</span><span class="p">,</span> <span class="n">fill_value</span><span class="o">=</span><span class="s1">&#39;missing&#39;</span><span class="p">)),</span>
    <span class="p">(</span><span class="s1">&#39;onehot&#39;</span><span class="p">,</span> <span class="n">OneHotEncoder</span><span class="p">(</span><span class="n">handle_unknown</span><span class="o">=</span><span class="s1">&#39;ignore&#39;</span><span class="p">))])</span>

<span class="n">preprocessor</span> <span class="o">=</span> <span class="n">ColumnTransformer</span><span class="p">(</span>
    <span class="n">transformers</span><span class="o">=</span><span class="p">[</span>
        <span class="p">(</span><span class="s1">&#39;num&#39;</span><span class="p">,</span> <span class="n">numeric_transformer</span><span class="p">,</span> <span class="n">numeric_features</span><span class="p">),</span>
        <span class="p">(</span><span class="s1">&#39;cat&#39;</span><span class="p">,</span> <span class="n">categorical_transformer</span><span class="p">,</span> <span class="n">categorical_features</span><span class="p">)])</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Models">Models<a class="anchor-link" href="#Models">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="Logistic-Regression">Logistic Regression<a class="anchor-link" href="#Logistic-Regression">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[21]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.linear_model</span> <span class="kn">import</span> <span class="n">LogisticRegression</span>

<span class="n">clf</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[(</span><span class="s1">&#39;preprocessor&#39;</span><span class="p">,</span> <span class="n">preprocessor</span><span class="p">),</span>
                      <span class="p">(</span><span class="s1">&#39;classifier&#39;</span><span class="p">,</span> <span class="n">LogisticRegression</span><span class="p">())])</span>

<span class="n">params</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;classifier__C&#39;</span><span class="p">:</span> <span class="n">np</span><span class="o">.</span><span class="n">linspace</span><span class="p">(</span><span class="mi">0</span><span class="p">,</span><span class="mi">1</span><span class="p">,</span><span class="mi">10</span><span class="p">)}</span>

<span class="n">grid</span> <span class="o">=</span> <span class="n">GridSearchCV</span><span class="p">(</span><span class="n">clf</span><span class="p">,</span> <span class="n">param_grid</span><span class="o">=</span><span class="n">params</span><span class="p">,</span> <span class="n">cv</span><span class="o">=</span><span class="mi">10</span><span class="p">)</span>

<span class="n">grid</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">X</span><span class="p">,</span> <span class="n">y</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,))</span>

<span class="nb">print</span><span class="p">(</span><span class="n">grid</span><span class="o">.</span><span class="n">best_score_</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">grid</span><span class="o">.</span><span class="n">best_params_</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>0.8193258426966292
{&#39;classifier__C&#39;: 0.8888888888888888}
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="Random-Forest-">Random Forest <a class="anchor" id="rf" /><a class="anchor-link" href="#Random-Forest-">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[22]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.ensemble</span> <span class="kn">import</span> <span class="n">RandomForestClassifier</span><span class="p">,</span> <span class="n">VotingClassifier</span>

<span class="n">random_grid_rf</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;classifier__n_estimators&#39;</span><span class="p">:</span> <span class="p">[</span><span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">np</span><span class="o">.</span><span class="n">linspace</span><span class="p">(</span><span class="n">start</span> <span class="o">=</span> <span class="mi">200</span><span class="p">,</span> <span class="n">stop</span> <span class="o">=</span> <span class="mi">2000</span><span class="p">,</span> <span class="n">num</span> <span class="o">=</span> <span class="mi">10</span><span class="p">)],</span>
               <span class="s1">&#39;classifier__max_features&#39;</span><span class="p">:</span> <span class="p">[</span><span class="s1">&#39;auto&#39;</span><span class="p">,</span> <span class="s1">&#39;sqrt&#39;</span><span class="p">],</span>
               <span class="s1">&#39;classifier__max_depth&#39;</span><span class="p">:</span> <span class="p">[</span><span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">np</span><span class="o">.</span><span class="n">linspace</span><span class="p">(</span><span class="mi">10</span><span class="p">,</span> <span class="mi">110</span><span class="p">,</span> <span class="n">num</span> <span class="o">=</span> <span class="mi">11</span><span class="p">)],</span>
               <span class="s1">&#39;classifier__min_samples_split&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">2</span><span class="p">,</span> <span class="mi">5</span><span class="p">,</span> <span class="mi">10</span><span class="p">],</span>
               <span class="s1">&#39;classifier__min_samples_leaf&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">2</span><span class="p">,</span> <span class="mi">4</span><span class="p">],</span>
               <span class="s1">&#39;classifier__bootstrap&#39;</span><span class="p">:</span> <span class="p">[</span><span class="kc">True</span><span class="p">,</span> <span class="kc">False</span><span class="p">]}</span>


<span class="n">clf</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[(</span><span class="s1">&#39;preprocessor&#39;</span><span class="p">,</span> <span class="n">preprocessor</span><span class="p">),</span>
                      <span class="p">(</span><span class="s1">&#39;classifier&#39;</span><span class="p">,</span> <span class="n">RandomForestClassifier</span><span class="p">())])</span>


<span class="n">rf_random</span> <span class="o">=</span> <span class="n">RandomizedSearchCV</span><span class="p">(</span><span class="n">estimator</span> <span class="o">=</span> <span class="n">clf</span><span class="p">,</span> <span class="n">param_distributions</span> <span class="o">=</span> <span class="n">random_grid_rf</span><span class="p">,</span> <span class="n">n_iter</span> <span class="o">=</span> <span class="mi">200</span><span class="p">,</span> <span class="n">cv</span> <span class="o">=</span> <span class="mi">10</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">random_state</span><span class="o">=</span><span class="mi">42</span><span class="p">,</span> <span class="n">n_jobs</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>

<span class="n">rf_random</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">X</span><span class="p">,</span> <span class="n">y</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,))</span>

<span class="nb">print</span><span class="p">(</span><span class="n">rf_random</span><span class="o">.</span><span class="n">best_score_</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">rf_random</span><span class="o">.</span><span class="n">best_params_</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Fitting 10 folds for each of 200 candidates, totalling 2000 fits
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stderr output_text">
<pre>[Parallel(n_jobs=-1)]: Using backend LokyBackend with 12 concurrent workers.
[Parallel(n_jobs=-1)]: Done  17 tasks      | elapsed:   14.8s
[Parallel(n_jobs=-1)]: Done 138 tasks      | elapsed:  2.4min
[Parallel(n_jobs=-1)]: Done 341 tasks      | elapsed:  4.9min
[Parallel(n_jobs=-1)]: Done 624 tasks      | elapsed: 11.3min
[Parallel(n_jobs=-1)]: Done 989 tasks      | elapsed: 19.0min
[Parallel(n_jobs=-1)]: Done 1434 tasks      | elapsed: 22.0min
[Parallel(n_jobs=-1)]: Done 1961 tasks      | elapsed: 27.3min
[Parallel(n_jobs=-1)]: Done 2000 out of 2000 | elapsed: 27.5min finished
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>0.827191011235955
{&#39;classifier__n_estimators&#39;: 200, &#39;classifier__min_samples_split&#39;: 2, &#39;classifier__min_samples_leaf&#39;: 2, &#39;classifier__max_features&#39;: &#39;sqrt&#39;, &#39;classifier__max_depth&#39;: 80, &#39;classifier__bootstrap&#39;: False}
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[27]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">joblib</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">rf_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">,</span> <span class="s1">&#39;best_rf.pickle&#39;</span><span class="p">)</span>

<span class="n">solution_df</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">column_stack</span><span class="p">((</span><span class="n">test</span><span class="o">.</span><span class="n">PassengerId</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="n">rf_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">test</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Ticket&#39;</span><span class="p">,</span> <span class="s1">&#39;Name&#39;</span><span class="p">])))),</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;PassengerId&#39;</span><span class="p">,</span> <span class="s1">&#39;Survived&#39;</span><span class="p">])</span>
<span class="n">solution_df</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="s1">&#39;solution_rf.csv&#39;</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="SVC-">SVC <a class="anchor" id="svc" /><a class="anchor-link" href="#SVC-">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[28]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.svm</span> <span class="kn">import</span> <span class="n">SVC</span>

<span class="n">random_grid_svc</span> <span class="o">=</span> <span class="p">{</span><span class="s1">&#39;classifier__kernel&#39;</span><span class="p">:</span> <span class="p">[</span><span class="s1">&#39;linear&#39;</span><span class="p">,</span> <span class="s1">&#39;rbf&#39;</span><span class="p">,</span> <span class="s1">&#39;poly&#39;</span><span class="p">],</span>
               <span class="s1">&#39;classifier__gamma&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">0.1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">10</span><span class="p">,</span> <span class="mi">20</span><span class="p">],</span>
               <span class="s1">&#39;classifier__C&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mf">0.1</span><span class="p">,</span> <span class="mi">1</span><span class="p">,</span> <span class="mi">10</span><span class="p">,</span> <span class="mi">100</span><span class="p">],</span>
              <span class="p">}</span>

<span class="n">clf</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[(</span><span class="s1">&#39;preprocessor&#39;</span><span class="p">,</span> <span class="n">preprocessor</span><span class="p">),</span>
                      <span class="p">(</span><span class="s1">&#39;classifier&#39;</span><span class="p">,</span> <span class="n">SVC</span><span class="p">())])</span>

<span class="n">svc_random</span> <span class="o">=</span> <span class="n">RandomizedSearchCV</span><span class="p">(</span><span class="n">estimator</span> <span class="o">=</span> <span class="n">clf</span><span class="p">,</span> <span class="n">param_distributions</span> <span class="o">=</span> <span class="n">random_grid_svc</span><span class="p">,</span> <span class="n">n_iter</span> <span class="o">=</span> <span class="mi">100</span><span class="p">,</span> <span class="n">cv</span> <span class="o">=</span> <span class="mi">3</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">random_state</span><span class="o">=</span><span class="mi">42</span><span class="p">,</span> <span class="n">n_jobs</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>

<span class="n">svc_random</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">X</span><span class="p">,</span> <span class="n">y</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,))</span>

<span class="nb">print</span><span class="p">(</span><span class="n">svc_random</span><span class="o">.</span><span class="n">best_score_</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">svc_random</span><span class="o">.</span><span class="n">best_params_</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Fitting 3 folds for each of 48 candidates, totalling 144 fits
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stderr output_text">
<pre>[Parallel(n_jobs=-1)]: Using backend LokyBackend with 12 concurrent workers.
[Parallel(n_jobs=-1)]: Done  17 tasks      | elapsed:    1.9s
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>0.8204264870931537
{&#39;classifier__kernel&#39;: &#39;poly&#39;, &#39;classifier__gamma&#39;: 0.1, &#39;classifier__C&#39;: 1}
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stderr output_text">
<pre>[Parallel(n_jobs=-1)]: Done 144 out of 144 | elapsed: 22.0min finished
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[29]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">joblib</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">svc_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">,</span> <span class="s1">&#39;best_svc.pickle&#39;</span><span class="p">)</span>

<span class="n">solution_df_svc</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">column_stack</span><span class="p">((</span><span class="n">test</span><span class="o">.</span><span class="n">PassengerId</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="n">svc_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">test</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Ticket&#39;</span><span class="p">,</span> <span class="s1">&#39;Name&#39;</span><span class="p">])))),</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;PassengerId&#39;</span><span class="p">,</span> <span class="s1">&#39;Survived&#39;</span><span class="p">])</span>
<span class="n">solution_df_svc</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="s1">&#39;solution_svc.csv&#39;</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="MLP-">MLP <a class="anchor" id="mlp" /><a class="anchor-link" href="#MLP-">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[30]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">from</span> <span class="nn">sklearn.neural_network</span> <span class="kn">import</span> <span class="n">MLPClassifier</span> 

<span class="n">random_grid_mlp</span> <span class="o">=</span> <span class="p">{</span>
                   <span class="s1">&#39;classifier__hidden_layer_sizes&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">32</span><span class="p">,</span> <span class="mi">64</span><span class="p">,</span> <span class="mi">128</span><span class="p">,</span> <span class="mi">256</span><span class="p">,</span> <span class="mi">512</span><span class="p">],</span>
                   <span class="s1">&#39;classifier__activation&#39;</span><span class="p">:</span> <span class="p">[</span><span class="s1">&#39;identity&#39;</span><span class="p">,</span> <span class="s1">&#39;logistic&#39;</span><span class="p">,</span> <span class="s1">&#39;tanh&#39;</span><span class="p">,</span> <span class="s1">&#39;relu&#39;</span><span class="p">],</span>
                   <span class="s1">&#39;classifier__solver&#39;</span><span class="p">:</span> <span class="p">[</span><span class="s1">&#39;lbfgs&#39;</span><span class="p">,</span> <span class="s1">&#39;sgd&#39;</span><span class="p">,</span> <span class="s1">&#39;adam&#39;</span><span class="p">],</span>
                   <span class="s1">&#39;classifier__alpha&#39;</span><span class="p">:</span> <span class="p">[</span><span class="o">.</span><span class="mi">00001</span><span class="p">,</span> <span class="o">.</span><span class="mi">0001</span><span class="p">,</span> <span class="o">.</span><span class="mi">001</span><span class="p">,</span> <span class="o">.</span><span class="mi">01</span><span class="p">],</span>
                   <span class="s1">&#39;classifier__learning_rate&#39;</span><span class="p">:</span> <span class="p">[</span><span class="s1">&#39;constant&#39;</span><span class="p">,</span> <span class="s1">&#39;invscaling&#39;</span><span class="p">,</span> <span class="s1">&#39;adaptive&#39;</span><span class="p">],</span>
                <span class="p">}</span>


<span class="n">clf</span> <span class="o">=</span> <span class="n">Pipeline</span><span class="p">(</span><span class="n">steps</span><span class="o">=</span><span class="p">[(</span><span class="s1">&#39;preprocessor&#39;</span><span class="p">,</span> <span class="n">preprocessor</span><span class="p">),</span>
                      <span class="p">(</span><span class="s1">&#39;classifier&#39;</span><span class="p">,</span> <span class="n">MLPClassifier</span><span class="p">(</span><span class="n">max_iter</span><span class="o">=</span><span class="mi">500</span><span class="p">))])</span>


<span class="n">mlp_random</span> <span class="o">=</span> <span class="n">RandomizedSearchCV</span><span class="p">(</span><span class="n">estimator</span> <span class="o">=</span> <span class="n">clf</span><span class="p">,</span> <span class="n">param_distributions</span> <span class="o">=</span> <span class="n">random_grid_mlp</span><span class="p">,</span> <span class="n">n_iter</span> <span class="o">=</span> <span class="mi">100</span><span class="p">,</span> <span class="n">cv</span> <span class="o">=</span> <span class="mi">3</span><span class="p">,</span> <span class="n">verbose</span><span class="o">=</span><span class="mi">2</span><span class="p">,</span> <span class="n">random_state</span><span class="o">=</span><span class="mi">42</span><span class="p">,</span> <span class="n">n_jobs</span> <span class="o">=</span> <span class="o">-</span><span class="mi">1</span><span class="p">)</span>

<span class="n">mlp_random</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">X</span><span class="p">,</span> <span class="n">y</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,))</span>

<span class="nb">print</span><span class="p">(</span><span class="n">mlp_random</span><span class="o">.</span><span class="n">best_score_</span><span class="p">)</span>
<span class="nb">print</span><span class="p">(</span><span class="n">mlp_random</span><span class="o">.</span><span class="n">best_params_</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>Fitting 3 folds for each of 100 candidates, totalling 300 fits
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stderr output_text">
<pre>[Parallel(n_jobs=-1)]: Using backend LokyBackend with 12 concurrent workers.
[Parallel(n_jobs=-1)]: Done  17 tasks      | elapsed:    9.2s
[Parallel(n_jobs=-1)]: Done 138 tasks      | elapsed:  4.0min
[Parallel(n_jobs=-1)]: Done 300 out of 300 | elapsed:  7.4min finished
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>0.8114478114478114
{&#39;classifier__solver&#39;: &#39;adam&#39;, &#39;classifier__learning_rate&#39;: &#39;adaptive&#39;, &#39;classifier__hidden_layer_sizes&#39;: 32, &#39;classifier__alpha&#39;: 0.01, &#39;classifier__activation&#39;: &#39;tanh&#39;}
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[31]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">joblib</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">mlp_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">,</span> <span class="s1">&#39;best_mlp.pickle&#39;</span><span class="p">)</span>

<span class="n">solution_df_mlp</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">column_stack</span><span class="p">((</span><span class="n">test</span><span class="o">.</span><span class="n">PassengerId</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="n">mlp_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">test</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Ticket&#39;</span><span class="p">,</span> <span class="s1">&#39;Name&#39;</span><span class="p">])))),</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;PassengerId&#39;</span><span class="p">,</span> <span class="s1">&#39;Survived&#39;</span><span class="p">])</span>
<span class="n">solution_df_mlp</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="s1">&#39;solution_mlp.csv&#39;</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="Voting-Classifier-">Voting Classifier <a class="anchor" id="vc" /><a class="anchor-link" href="#Voting-Classifier-">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[32]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">v</span> <span class="o">=</span> <span class="n">VotingClassifier</span><span class="p">([(</span><span class="s1">&#39;log&#39;</span><span class="p">,</span> <span class="n">grid</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">),</span> <span class="p">(</span><span class="s1">&#39;rf&#39;</span><span class="p">,</span> <span class="n">rf_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">),</span> <span class="p">(</span><span class="s1">&#39;svc&#39;</span><span class="p">,</span> <span class="n">svc_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">),</span> <span class="p">(</span><span class="s1">&#39;mlp&#39;</span><span class="p">,</span> <span class="n">mlp_random</span><span class="o">.</span><span class="n">best_estimator_</span><span class="p">)])</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[34]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">v</span><span class="o">.</span><span class="n">fit</span><span class="p">(</span><span class="n">X</span><span class="p">,</span> <span class="n">y</span><span class="o">.</span><span class="n">values</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,))</span>
<span class="nb">print</span><span class="p">(</span><span class="n">accuracy_score</span><span class="p">(</span><span class="n">v</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">X</span><span class="p">),</span> <span class="n">y</span><span class="p">))</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>0.8552188552188552
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[36]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">joblib</span><span class="o">.</span><span class="n">dump</span><span class="p">(</span><span class="n">v</span><span class="p">,</span> <span class="s1">&#39;best_vc.pickle&#39;</span><span class="p">)</span>

<span class="n">solution_df_v</span> <span class="o">=</span> <span class="n">pd</span><span class="o">.</span><span class="n">DataFrame</span><span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">column_stack</span><span class="p">((</span><span class="n">test</span><span class="o">.</span><span class="n">PassengerId</span><span class="o">.</span><span class="n">values</span><span class="p">,</span> <span class="n">v</span><span class="o">.</span><span class="n">predict</span><span class="p">(</span><span class="n">test</span><span class="o">.</span><span class="n">drop</span><span class="p">(</span><span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;Ticket&#39;</span><span class="p">,</span> <span class="s1">&#39;Name&#39;</span><span class="p">])))),</span> <span class="n">columns</span><span class="o">=</span><span class="p">[</span><span class="s1">&#39;PassengerId&#39;</span><span class="p">,</span> <span class="s1">&#39;Survived&#39;</span><span class="p">])</span>
<span class="n">solution_df_v</span><span class="o">.</span><span class="n">to_csv</span><span class="p">(</span><span class="s1">&#39;solution_voting_classifier.csv&#39;</span><span class="p">,</span> <span class="n">index</span><span class="o">=</span><span class="kc">False</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="Submit-to-Kaggle">Submit to Kaggle<a class="anchor-link" href="#Submit-to-Kaggle">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[41]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">os</span>
<span class="n">os</span><span class="o">.</span><span class="n">system</span><span class="p">(</span><span class="s2">&quot;kaggle competitions submit -c titanic -f submission.csv -m &#39;Voting Classifier with sklearn Pipeline preprocessing&#39;&quot;</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt output_prompt">Out[41]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>32512</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[&nbsp;]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span>
</pre></div>

    </div>
</div>
</div>

</div>
 

