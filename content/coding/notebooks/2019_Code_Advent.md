title: "2019 Advent of Code"
details: "Partial solutions to 2019 Advent of Code"
date: 2019-02-25
lastmod: 2019-02-25

<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h1 id="Advent-of-Code-2019-Python-Solutions">Advent of Code 2019 Python Solutions<a class="anchor-link" href="#Advent-of-Code-2019-Python-Solutions">&#182;</a></h1><p>Samuel Mignot's solution for <a href="https://adventofcode.com/">the 2019 Advent of Code challenge</a>.</p>
<p>Have yet to get through the entire challenge, but slowly working my way throuh it.
The intcode computer, which is created and used in multiple challenges, is abstracted into an intcomp.py file.</p>

</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Global-Setup">Global Setup<a class="anchor-link" href="#Global-Setup">&#182;</a></h2><p>Handles imports, notebook magic, and notebook-wide constants</p>

</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="imports">imports<a class="anchor-link" href="#imports">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[7]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="kn">import</span> <span class="nn">string</span>
<span class="kn">import</span> <span class="nn">numpy</span> <span class="k">as</span> <span class="nn">np</span>
<span class="kn">from</span> <span class="nn">itertools</span> <span class="kn">import</span> <span class="n">cycle</span>
<span class="kn">import</span> <span class="nn">requests</span>
<span class="kn">import</span> <span class="nn">collections</span>
<span class="kn">from</span> <span class="nn">collections</span> <span class="kn">import</span> <span class="n">deque</span>
<span class="kn">from</span> <span class="nn">pprint</span> <span class="kn">import</span> <span class="n">pprint</span>
<span class="kn">import</span> <span class="nn">operator</span>
<span class="kn">from</span> <span class="nn">time</span> <span class="kn">import</span> <span class="n">sleep</span>
<span class="kn">import</span> <span class="nn">itertools</span>
<span class="kn">import</span> <span class="nn">re</span>
<span class="kn">import</span> <span class="nn">functools</span>
<span class="kn">from</span> <span class="nn">functools</span> <span class="kn">import</span> <span class="n">reduce</span>
<span class="kn">from</span> <span class="nn">dataclasses</span> <span class="kn">import</span> <span class="n">dataclass</span>
<span class="kn">from</span> <span class="nn">copy</span> <span class="kn">import</span> <span class="n">deepcopy</span>
<span class="kn">import</span> <span class="nn">networkx</span> <span class="k">as</span> <span class="nn">nx</span>
<span class="kn">import</span> <span class="nn">matplotlib.pyplot</span> <span class="k">as</span> <span class="nn">plt</span>
<span class="kn">import</span> <span class="nn">intcomp</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="notebook-magic">notebook magic<a class="anchor-link" href="#notebook-magic">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[8]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%</span><span class="n">matplotlib</span> <span class="n">widget</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="constants">constants<a class="anchor-link" href="#constants">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[9]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">LOWERCASE</span> <span class="o">=</span> <span class="n">string</span><span class="o">.</span><span class="n">ascii_lowercase</span>
<span class="n">UPPERCASE</span> <span class="o">=</span> <span class="n">string</span><span class="o">.</span><span class="n">ascii_uppercase</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="helpers">helpers<a class="anchor-link" href="#helpers">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[10]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="k">def</span> <span class="nf">get_level_input</span><span class="p">(</span><span class="n">lvl_num</span><span class="p">):</span>
    <span class="k">with</span> <span class="nb">open</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;advent_inputs/</span><span class="si">{</span><span class="n">lvl_num</span><span class="si">}</span><span class="s2">.txt&quot;</span><span class="p">)</span> <span class="k">as</span> <span class="n">f</span><span class="p">:</span>
        <span class="n">level_input</span><span class="o">=</span><span class="n">f</span><span class="o">.</span><span class="n">read</span><span class="p">()</span>
        <span class="k">return</span> <span class="n">level_input</span>
    
<span class="k">def</span> <span class="nf">print_result</span><span class="p">(</span><span class="n">answer</span><span class="p">):</span>
    <span class="n">pprint</span><span class="p">(</span><span class="s2">&quot;RESULT: &quot;</span><span class="o">+</span><span class="nb">str</span><span class="p">(</span><span class="n">answer</span><span class="p">))</span>
    <span class="nb">print</span><span class="p">()</span>
    <span class="n">pprint</span><span class="p">(</span><span class="s2">&quot;TIME&quot;</span><span class="o">+</span><span class="s2">&quot;.&quot;</span><span class="o">*</span><span class="mi">60</span><span class="p">)</span>
    
<span class="k">class</span> <span class="nc">StopExecution</span><span class="p">(</span><span class="ne">Exception</span><span class="p">):</span>
    <span class="k">def</span> <span class="nf">_render_traceback_</span><span class="p">(</span><span class="bp">self</span><span class="p">):</span>
        <span class="k">pass</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-1:-The-Tyranny-of-the-Rocket-Equation">Day 1: The Tyranny of the Rocket Equation<a class="anchor-link" href="#Day-1:-The-Tyranny-of-the-Rocket-Equation">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[11]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">module_weights</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;01&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">splitlines</span><span class="p">()</span>
<span class="n">module_weights</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">module_weights</span><span class="p">))</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[12]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">total_weight</span> <span class="o">=</span> <span class="nb">sum</span><span class="p">([</span><span class="n">x</span><span class="o">//</span><span class="mi">3</span> <span class="o">-</span> <span class="mi">2</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">module_weights</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">total_weight</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 3432671&#39;

&#39;TIME............................................................&#39;
CPU times: user 128 µs, sys: 34 µs, total: 162 µs
Wall time: 145 µs
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[13]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="k">def</span> <span class="nf">weight_of_weight_gen</span><span class="p">(</span><span class="n">m_weight</span><span class="p">):</span>
    <span class="k">while</span> <span class="n">m_weight</span><span class="o">&gt;</span><span class="mi">0</span><span class="p">:</span>
        <span class="k">yield</span> <span class="n">m_weight</span>
        <span class="n">m_weight</span> <span class="o">=</span> <span class="n">m_weight</span><span class="o">//</span><span class="mi">3</span> <span class="o">-</span> <span class="mi">2</span>
    
<span class="k">def</span> <span class="nf">get_req_fuel</span><span class="p">(</span><span class="n">m_weight</span><span class="p">):</span> 
    <span class="k">return</span> <span class="nb">sum</span><span class="p">([</span><span class="n">i</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="n">weight_of_weight_gen</span><span class="p">(</span><span class="n">m_weight</span><span class="p">)][</span><span class="mi">1</span><span class="p">:])</span>
    
<span class="n">total_weight</span> <span class="o">=</span> <span class="nb">sum</span><span class="p">([</span><span class="n">get_req_fuel</span><span class="p">(</span><span class="n">x</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">module_weights</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">total_weight</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 5146132&#39;

&#39;TIME............................................................&#39;
CPU times: user 373 µs, sys: 47 µs, total: 420 µs
Wall time: 397 µs
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-2:-1202-Program-Alarm">Day 2: 1202 Program Alarm<a class="anchor-link" href="#Day-2:-1202-Program-Alarm">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[14]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">comp_string</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;02&quot;</span><span class="p">)</span>
<span class="n">comp_string</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">comp_string</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)))</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[15]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">comp_string_prog</span> <span class="o">=</span> <span class="n">comp_string</span><span class="p">[:]</span>
<span class="n">comp_string_prog</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span> <span class="o">=</span> <span class="mi">12</span>
<span class="n">comp_string_prog</span><span class="p">[</span><span class="mi">2</span><span class="p">]</span> <span class="o">=</span> <span class="mi">2</span>
<span class="n">res</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">comp_string_prog</span><span class="p">,</span> <span class="p">[])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">comp_string_prog</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 5290681&#39;

&#39;TIME............................................................&#39;
CPU times: user 582 µs, sys: 271 µs, total: 853 µs
Wall time: 608 µs
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[&nbsp;]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">TARGET</span> <span class="o">=</span> <span class="mi">19690720</span>
<span class="n">NOUN_POS</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">VERB_POS</span> <span class="o">=</span> <span class="mi">2</span>
    
<span class="k">def</span> <span class="nf">find_noun_verb</span><span class="p">(</span><span class="n">comp_string</span><span class="p">):</span>
    <span class="k">for</span> <span class="n">noun</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">100</span><span class="p">):</span>
        <span class="k">for</span> <span class="n">verb</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">100</span><span class="p">):</span>
            <span class="n">comp_string_copy</span> <span class="o">=</span> <span class="n">comp_string</span><span class="p">[:]</span>
            <span class="n">comp_string_copy</span><span class="p">[</span><span class="n">NOUN_POS</span><span class="p">]</span> <span class="o">=</span> <span class="n">noun</span>
            <span class="n">comp_string_copy</span><span class="p">[</span><span class="n">VERB_POS</span><span class="p">]</span> <span class="o">=</span> <span class="n">verb</span>
            <span class="n">res</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">comp_string_copy</span><span class="p">,</span> <span class="p">[])</span> 
            <span class="k">if</span> <span class="n">comp_string_copy</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="o">-</span><span class="mi">1</span><span class="p">:</span> <span class="k">continue</span> 
            <span class="k">if</span><span class="p">(</span><span class="n">comp_string_copy</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span> <span class="o">==</span> <span class="n">TARGET</span><span class="p">):</span> <span class="k">return</span> <span class="n">noun</span><span class="p">,</span><span class="n">verb</span>

<span class="n">noun</span><span class="p">,</span> <span class="n">verb</span> <span class="o">=</span> <span class="n">find_noun_verb</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="n">comp_string</span><span class="p">))</span>

<span class="n">print_result</span><span class="p">(</span><span class="mi">100</span> <span class="o">*</span> <span class="n">noun</span> <span class="o">+</span> <span class="n">verb</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-3:-Crossed-Wires">Day 3: Crossed Wires<a class="anchor-link" href="#Day-3:-Crossed-Wires">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[11]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">wires_input</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;03&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">splitlines</span><span class="p">()</span>
<span class="n">wires_input</span> <span class="o">=</span> <span class="p">[</span><span class="n">x</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">wires_input</span><span class="p">]</span>

<span class="n">X</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">Y</span> <span class="o">=</span> <span class="mi">0</span>
<span class="n">CENTER_POINT</span> <span class="o">=</span> <span class="p">(</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">)</span>

<span class="k">def</span> <span class="nf">md</span><span class="p">(</span><span class="n">p1</span><span class="p">,</span> <span class="n">p2</span><span class="p">):</span>
    <span class="k">return</span> <span class="p">(</span><span class="nb">abs</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="o">+</span> <span class="nb">abs</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">]))</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[12]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="k">def</span> <span class="nf">generate_wire</span><span class="p">(</span><span class="n">instructions</span><span class="p">):</span>
    <span class="n">wire</span> <span class="o">=</span> <span class="p">[</span><span class="n">CENTER_POINT</span><span class="p">]</span>
    <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">instructions</span><span class="p">:</span>
        <span class="n">cur_point</span> <span class="o">=</span> <span class="n">wire</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
        <span class="n">wire</span> <span class="o">+=</span> <span class="p">{</span>
         <span class="s1">&#39;U&#39;</span><span class="p">:</span> <span class="p">[(</span><span class="n">cur_point</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">i</span><span class="p">,</span> <span class="n">cur_point</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">:])</span><span class="o">+</span><span class="mi">1</span><span class="p">)],</span>
         <span class="s1">&#39;D&#39;</span><span class="p">:</span> <span class="p">[(</span><span class="n">cur_point</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">+</span><span class="n">i</span><span class="p">,</span> <span class="n">cur_point</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">:])</span><span class="o">+</span><span class="mi">1</span><span class="p">)],</span>
         <span class="s1">&#39;L&#39;</span><span class="p">:</span> <span class="p">[(</span><span class="n">cur_point</span><span class="p">[</span><span class="n">Y</span><span class="p">],</span> <span class="n">cur_point</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">i</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">:])</span><span class="o">+</span><span class="mi">1</span><span class="p">)],</span>
         <span class="s1">&#39;R&#39;</span><span class="p">:</span> <span class="p">[(</span><span class="n">cur_point</span><span class="p">[</span><span class="n">Y</span><span class="p">],</span> <span class="n">cur_point</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">+</span><span class="n">i</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">int</span><span class="p">(</span><span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">:])</span><span class="o">+</span><span class="mi">1</span><span class="p">)]</span>
        <span class="p">}[</span><span class="n">x</span><span class="p">[</span><span class="mi">0</span><span class="p">]]</span>
    <span class="k">return</span> <span class="n">wire</span>
                                  
    
<span class="n">wires</span> <span class="o">=</span> <span class="p">[</span><span class="nb">set</span><span class="p">(</span><span class="n">generate_wire</span><span class="p">(</span><span class="n">w_i</span><span class="p">))</span><span class="o">-</span><span class="p">{</span><span class="n">CENTER_POINT</span><span class="p">}</span> <span class="k">for</span> <span class="n">w_i</span> <span class="ow">in</span> <span class="n">wires_input</span><span class="p">]</span>
<span class="n">res</span> <span class="o">=</span> <span class="nb">min</span><span class="p">([</span><span class="n">md</span><span class="p">(</span><span class="n">x</span><span class="p">,</span> <span class="n">CENTER_POINT</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">set</span><span class="o">.</span><span class="n">intersection</span><span class="p">(</span><span class="o">*</span><span class="n">wires</span><span class="p">)])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">res</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 225&#39;

&#39;TIME............................................................&#39;
CPU times: user 302 ms, sys: 20.5 ms, total: 322 ms
Wall time: 323 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[13]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">wires</span> <span class="o">=</span> <span class="p">[</span><span class="n">generate_wire</span><span class="p">(</span><span class="n">w_i</span><span class="p">)</span> <span class="k">for</span> <span class="n">w_i</span> <span class="ow">in</span> <span class="n">wires_input</span><span class="p">]</span>
<span class="n">intersections</span> <span class="o">=</span> <span class="nb">set</span><span class="o">.</span><span class="n">intersection</span><span class="p">(</span><span class="o">*</span><span class="p">[</span><span class="nb">set</span><span class="p">(</span><span class="n">wire</span><span class="p">)</span> <span class="k">for</span> <span class="n">wire</span> <span class="ow">in</span> <span class="n">wires</span><span class="p">])</span><span class="o">-</span><span class="p">{</span><span class="n">CENTER_POINT</span><span class="p">}</span>
<span class="n">res</span> <span class="o">=</span> <span class="nb">min</span><span class="p">([</span><span class="n">wires</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">index</span><span class="p">(</span><span class="n">x</span><span class="p">)</span><span class="o">+</span><span class="n">wires</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">.</span><span class="n">index</span><span class="p">(</span><span class="n">x</span><span class="p">)</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="n">intersections</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">res</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 35194&#39;

&#39;TIME............................................................&#39;
CPU times: user 449 ms, sys: 19.5 ms, total: 468 ms
Wall time: 470 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-4:-Secure-Container">Day 4: Secure Container<a class="anchor-link" href="#Day-4:-Secure-Container">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[14]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">r_low</span><span class="p">,</span> <span class="n">r_high</span> <span class="o">=</span> <span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;04&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s2">&quot;-&quot;</span><span class="p">))</span>

<span class="k">def</span> <span class="nf">check_value</span><span class="p">(</span><span class="n">val</span><span class="p">,</span> <span class="n">functions</span><span class="p">):</span>
    <span class="n">num_list</span> <span class="o">=</span> <span class="p">[</span><span class="nb">int</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">list</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">val</span><span class="p">))]</span>
    <span class="k">return</span> <span class="p">(</span><span class="nb">all</span><span class="p">(</span><span class="n">f</span><span class="p">(</span><span class="n">num_list</span><span class="p">)</span> <span class="k">for</span> <span class="n">f</span> <span class="ow">in</span> <span class="n">functions</span><span class="p">))</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[15]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="k">def</span> <span class="nf">check_increase</span><span class="p">(</span><span class="n">l</span><span class="p">):</span>
    <span class="k">return</span> <span class="nb">all</span><span class="p">(</span><span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">l</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>

<span class="k">def</span> <span class="nf">check_double</span><span class="p">(</span><span class="n">l</span><span class="p">):</span>
    <span class="k">return</span> <span class="nb">any</span><span class="p">(</span><span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">==</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">l</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>

<span class="n">num_poss_pass</span> <span class="o">=</span> <span class="mi">0</span>
<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">r_low</span><span class="p">,</span> <span class="n">r_high</span><span class="o">+</span><span class="mi">1</span><span class="p">):</span>
    <span class="k">if</span><span class="p">(</span><span class="n">check_value</span><span class="p">(</span><span class="n">num</span><span class="p">,</span> <span class="p">[</span><span class="n">check_increase</span><span class="p">,</span> <span class="n">check_double</span><span class="p">])):</span> <span class="n">num_poss_pass</span><span class="o">+=</span><span class="mi">1</span>

<span class="n">print_result</span><span class="p">(</span><span class="n">num_poss_pass</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 1694&#39;

&#39;TIME............................................................&#39;
CPU times: user 1.74 s, sys: 10.6 ms, total: 1.75 s
Wall time: 1.76 s
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[16]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="k">def</span> <span class="nf">check_increase</span><span class="p">(</span><span class="n">l</span><span class="p">):</span>
    <span class="k">return</span> <span class="nb">all</span><span class="p">(</span><span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">&lt;=</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="nb">len</span><span class="p">(</span><span class="n">l</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>

<span class="k">def</span> <span class="nf">check_ungrouped_double</span><span class="p">(</span><span class="n">l</span><span class="p">):</span>
    <span class="n">l</span> <span class="o">=</span> <span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">+</span> <span class="n">l</span> <span class="o">+</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
    <span class="k">return</span> <span class="nb">any</span><span class="p">(</span><span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span> <span class="o">!=</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="p">]</span> <span class="o">==</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="o">!=</span> <span class="n">l</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">2</span><span class="p">]</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">1</span><span class="p">,</span> <span class="nb">len</span><span class="p">(</span><span class="n">l</span><span class="p">)</span><span class="o">-</span><span class="mi">1</span><span class="p">))</span>

<span class="n">num_poss_pass</span> <span class="o">=</span> <span class="mi">0</span>
<span class="k">for</span> <span class="n">num</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">r_low</span><span class="p">,</span> <span class="n">r_high</span><span class="o">+</span><span class="mi">1</span><span class="p">):</span>
    <span class="n">num_list</span> <span class="o">=</span> <span class="p">[</span><span class="nb">int</span><span class="p">(</span><span class="n">i</span><span class="p">)</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">list</span><span class="p">(</span><span class="nb">str</span><span class="p">(</span><span class="n">num</span><span class="p">))]</span>
    <span class="k">if</span><span class="p">(</span><span class="n">check_value</span><span class="p">(</span><span class="n">num</span><span class="p">,</span> <span class="p">[</span><span class="n">check_increase</span><span class="p">,</span> <span class="n">check_ungrouped_double</span><span class="p">])):</span> <span class="n">num_poss_pass</span> <span class="o">+=</span> <span class="mi">1</span>

<span class="n">print_result</span><span class="p">(</span><span class="n">num_poss_pass</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 1148&#39;

&#39;TIME............................................................&#39;
CPU times: user 2.6 s, sys: 13.9 ms, total: 2.61 s
Wall time: 2.63 s
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-5:-Sunny-with-a-Chance-of-Asteroids">Day 5: Sunny with a Chance of Asteroids<a class="anchor-link" href="#Day-5:-Sunny-with-a-Chance-of-Asteroids">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[17]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">comp_string</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;05&quot;</span><span class="p">)</span>
<span class="n">comp_string</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">comp_string</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)))</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[18]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">_</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">comp_string</span><span class="p">[:],</span> <span class="p">[</span><span class="mi">1</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">])</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 10987514&#39;

&#39;TIME............................................................&#39;
CPU times: user 288 µs, sys: 19 µs, total: 307 µs
Wall time: 297 µs
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[19]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">_</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">comp_string</span><span class="p">[:],</span> <span class="p">[</span><span class="mi">5</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 14195011&#39;

&#39;TIME............................................................&#39;
CPU times: user 643 µs, sys: 156 µs, total: 799 µs
Wall time: 681 µs
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-6:-Universal-Orbit-Map">Day 6: Universal Orbit Map<a class="anchor-link" href="#Day-6:-Universal-Orbit-Map">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[20]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">orbits</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;06&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">splitlines</span><span class="p">()</span>
<span class="n">orbits</span> <span class="o">=</span> <span class="p">[</span><span class="n">orbit</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;)&#39;</span><span class="p">)</span> <span class="k">for</span> <span class="n">orbit</span> <span class="ow">in</span> <span class="n">orbits</span><span class="p">]</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[21]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">orbit_graph</span> <span class="o">=</span> <span class="n">nx</span><span class="o">.</span><span class="n">DiGraph</span><span class="p">()</span>
<span class="k">for</span> <span class="n">orbit</span> <span class="ow">in</span> <span class="n">orbits</span><span class="p">:</span>
    <span class="n">orbit_graph</span><span class="o">.</span><span class="n">add_edge</span><span class="p">(</span><span class="o">*</span><span class="n">orbit</span><span class="p">)</span>

<span class="n">orbit_checksum</span> <span class="o">=</span> <span class="nb">sum</span><span class="p">([</span><span class="nb">len</span><span class="p">(</span><span class="n">nx</span><span class="o">.</span><span class="n">descendants</span><span class="p">(</span><span class="n">orbit_graph</span><span class="p">,</span> <span class="n">node</span><span class="p">))</span> <span class="k">for</span> <span class="n">node</span> <span class="ow">in</span> <span class="n">orbit_graph</span><span class="o">.</span><span class="n">nodes</span><span class="p">()])</span>

<span class="n">print_result</span><span class="p">(</span><span class="n">orbit_checksum</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 144909&#39;

&#39;TIME............................................................&#39;
CPU times: user 428 ms, sys: 5.79 ms, total: 434 ms
Wall time: 437 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[22]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">TARGET</span> <span class="o">=</span> <span class="s2">&quot;SAN&quot;</span>
<span class="n">START</span> <span class="o">=</span> <span class="s2">&quot;YOU&quot;</span>

<span class="n">orbit_graph</span> <span class="o">=</span> <span class="n">nx</span><span class="o">.</span><span class="n">Graph</span><span class="p">()</span>
<span class="k">for</span> <span class="n">orbit</span> <span class="ow">in</span> <span class="n">orbits</span><span class="p">:</span>
    <span class="n">orbit_graph</span><span class="o">.</span><span class="n">add_edge</span><span class="p">(</span><span class="o">*</span><span class="n">orbit</span><span class="p">)</span>

<span class="n">START_SR</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">orbit_graph</span><span class="o">.</span><span class="n">neighbors</span><span class="p">(</span><span class="n">START</span><span class="p">))[</span><span class="mi">0</span><span class="p">]</span>
<span class="n">SAN_SR</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">orbit_graph</span><span class="o">.</span><span class="n">neighbors</span><span class="p">(</span><span class="n">TARGET</span><span class="p">))[</span><span class="mi">0</span><span class="p">]</span>

<span class="n">print_result</span><span class="p">(</span><span class="n">nx</span><span class="o">.</span><span class="n">shortest_path_length</span><span class="p">(</span><span class="n">orbit_graph</span><span class="p">,</span> <span class="nb">str</span><span class="p">(</span><span class="n">START_SR</span><span class="p">),</span> <span class="nb">str</span><span class="p">(</span><span class="n">SAN_SR</span><span class="p">)))</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 259&#39;

&#39;TIME............................................................&#39;
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-7:-Amplification-Circuit">Day 7: Amplification Circuit<a class="anchor-link" href="#Day-7:-Amplification-Circuit">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[23]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">amp_prog</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;07&quot;</span><span class="p">)</span>
<span class="n">amp_prog</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">amp_prog</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)))</span>
<span class="n">NUM_AMPS</span> <span class="o">=</span> <span class="mi">5</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[24]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">amp_pos</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">itertools</span><span class="o">.</span><span class="n">permutations</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">))))</span>

<span class="n">max_val</span> <span class="o">=</span> <span class="mi">0</span>

<span class="k">for</span> <span class="n">perm</span> <span class="ow">in</span> <span class="n">amp_pos</span><span class="p">:</span>
    <span class="n">inputs</span> <span class="o">=</span> <span class="p">[</span><span class="n">perm</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="mi">0</span><span class="p">]</span>
    <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">):</span>
        <span class="n">inputs</span> <span class="o">=</span> <span class="p">[</span><span class="n">perm</span><span class="p">[</span><span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="p">]</span> <span class="k">if</span> <span class="n">i</span><span class="o">+</span><span class="mi">1</span><span class="o">&lt;</span><span class="n">NUM_AMPS</span> <span class="k">else</span> <span class="mi">0</span><span class="p">,</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">amp_prog</span><span class="p">[:],</span> <span class="n">inputs</span><span class="p">)[</span><span class="mi">1</span><span class="p">][</span><span class="mi">0</span><span class="p">]]</span>
        <span class="k">if</span><span class="p">(</span><span class="n">inputs</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span><span class="o">&gt;</span><span class="n">max_val</span><span class="p">):</span>
            <span class="n">max_val</span> <span class="o">=</span> <span class="n">inputs</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>
        
<span class="n">print_result</span><span class="p">(</span><span class="n">max_val</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 21760&#39;

&#39;TIME............................................................&#39;
CPU times: user 20.2 ms, sys: 1.01 ms, total: 21.2 ms
Wall time: 20.5 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[25]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">amp_pos</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">itertools</span><span class="o">.</span><span class="n">permutations</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">,</span> <span class="n">NUM_AMPS</span><span class="o">+</span><span class="mi">5</span><span class="p">))))</span>

<span class="n">signals</span> <span class="o">=</span> <span class="p">[]</span>
<span class="k">for</span> <span class="n">perm</span> <span class="ow">in</span> <span class="n">amp_pos</span><span class="p">:</span>
    <span class="n">i</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="n">inputs</span> <span class="o">=</span> <span class="p">[[</span><span class="n">perm</span><span class="p">[</span><span class="n">j</span><span class="p">]]</span> <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">)]</span>
    <span class="n">inputs</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="mi">0</span><span class="p">)</span>
    <span class="n">last_e</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="n">amp_progs</span> <span class="o">=</span> <span class="p">[</span><span class="n">deepcopy</span><span class="p">(</span><span class="n">amp_prog</span><span class="p">)</span> <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">)]</span>
    <span class="n">ips</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span> <span class="k">for</span> <span class="n">j</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">NUM_AMPS</span><span class="p">)]</span>
    <span class="k">while</span><span class="p">(</span><span class="kc">True</span><span class="p">):</span>
        <span class="n">ips</span><span class="p">[</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span><span class="p">],</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">amp_progs</span><span class="p">[</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span><span class="p">],</span> <span class="n">inputs</span><span class="p">[</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span><span class="p">],</span> <span class="n">ip</span><span class="o">=</span><span class="n">ips</span><span class="p">[</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span><span class="p">],</span> <span class="n">return_on_output</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">outputs</span> <span class="o">==</span> <span class="p">[]:</span>
            <span class="k">break</span>
        <span class="k">if</span><span class="p">(</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span> <span class="o">==</span> <span class="mi">4</span><span class="p">):</span>
            <span class="n">last_e</span> <span class="o">=</span> <span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span>
        <span class="n">i</span><span class="o">+=</span><span class="mi">1</span>
        <span class="n">inputs</span><span class="p">[</span><span class="n">i</span><span class="o">%</span><span class="n">NUM_AMPS</span><span class="p">]</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
    <span class="n">signals</span><span class="o">.</span><span class="n">append</span><span class="p">(</span><span class="n">last_e</span><span class="p">)</span>
        
<span class="n">print_result</span><span class="p">(</span><span class="nb">max</span><span class="p">(</span><span class="n">signals</span><span class="p">))</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 69816958&#39;

&#39;TIME............................................................&#39;
CPU times: user 252 ms, sys: 3.48 ms, total: 255 ms
Wall time: 256 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-8:-Space-Image-Format">Day 8: Space Image Format<a class="anchor-link" href="#Day-8:-Space-Image-Format">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[26]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">img</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;08&quot;</span><span class="p">))</span>
<span class="n">img</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">img</span><span class="p">))</span>
<span class="n">IMG_W</span> <span class="o">=</span> <span class="mi">25</span>
<span class="n">IMG_H</span> <span class="o">=</span> <span class="mi">6</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[27]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">arr_img</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">img</span><span class="p">)</span>
<span class="n">lay_img</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="n">arr_img</span><span class="p">,</span> <span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">IMG_H</span><span class="p">,</span> <span class="n">IMG_W</span><span class="p">))</span>

<span class="n">max_zero_index</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">argmin</span><span class="p">([(</span><span class="n">lay_img</span><span class="p">[</span><span class="n">i</span><span class="p">,:,:]</span><span class="o">==</span><span class="mi">0</span><span class="p">)</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span> <span class="k">for</span> <span class="n">i</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">lay_img</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">0</span><span class="p">])])</span>

<span class="n">max_zero_layer</span> <span class="o">=</span> <span class="n">lay_img</span><span class="p">[</span><span class="n">max_zero_index</span><span class="p">,</span> <span class="p">:,</span> <span class="p">:]</span>
<span class="n">NUM_1_BY_2</span> <span class="o">=</span> <span class="p">(</span><span class="n">max_zero_layer</span> <span class="o">==</span> <span class="mi">1</span><span class="p">)</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span> <span class="o">*</span> <span class="p">(</span><span class="n">max_zero_layer</span> <span class="o">==</span> <span class="mi">2</span><span class="p">)</span><span class="o">.</span><span class="n">sum</span><span class="p">()</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">NUM_1_BY_2</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 1360&#39;

&#39;TIME............................................................&#39;
CPU times: user 2.36 ms, sys: 314 µs, total: 2.67 ms
Wall time: 2.46 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[28]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">BLACK</span> <span class="o">=</span> <span class="mi">0</span> 
<span class="n">WHITE</span> <span class="o">=</span> <span class="mi">1</span> 
<span class="n">TRANS</span> <span class="o">=</span> <span class="mi">2</span>

<span class="n">arr_img</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">img</span><span class="p">)</span>
<span class="n">lay_img</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">reshape</span><span class="p">(</span><span class="n">arr_img</span><span class="p">,</span> <span class="p">(</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="n">IMG_H</span><span class="p">,</span> <span class="n">IMG_W</span><span class="p">))</span>

<span class="n">final_image</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">full</span><span class="p">((</span><span class="n">IMG_H</span><span class="p">,</span> <span class="n">IMG_W</span><span class="p">),</span> <span class="mi">2</span><span class="p">)</span>

<span class="n">spears</span> <span class="o">=</span> <span class="p">[</span><span class="n">lay_img</span><span class="p">[:,</span> <span class="n">col</span><span class="p">,</span> <span class="n">row</span><span class="p">]</span> <span class="k">for</span> <span class="n">col</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">lay_img</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">1</span><span class="p">])</span> <span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="n">lay_img</span><span class="o">.</span><span class="n">shape</span><span class="p">[</span><span class="mi">2</span><span class="p">])]</span>

<span class="n">first_non_transparent</span> <span class="o">=</span> <span class="p">[</span><span class="n">spear</span><span class="p">[</span><span class="n">np</span><span class="o">.</span><span class="n">argmax</span><span class="p">(</span><span class="n">spear</span><span class="o">!=</span><span class="mi">2</span><span class="p">)]</span> <span class="k">for</span> <span class="n">spear</span> <span class="ow">in</span> <span class="n">spears</span><span class="p">]</span>
<span class="n">message</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="n">first_non_transparent</span><span class="p">)</span><span class="o">.</span><span class="n">reshape</span><span class="p">((</span><span class="n">IMG_H</span><span class="p">,</span> <span class="n">IMG_W</span><span class="p">))</span>
<span class="k">for</span> <span class="n">row</span> <span class="ow">in</span> <span class="n">message</span><span class="p">:</span>
    <span class="n">row</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">where</span><span class="p">(</span><span class="n">row</span><span class="o">==</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;.&#39;</span><span class="p">,</span> <span class="n">row</span><span class="p">)</span> 
    <span class="n">row</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">where</span><span class="p">(</span><span class="n">row</span><span class="o">==</span><span class="s1">&#39;1&#39;</span><span class="p">,</span> <span class="s1">&#39;X&#39;</span><span class="p">,</span> <span class="n">row</span><span class="p">)</span> 
    <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;&quot;</span><span class="o">.</span><span class="n">join</span><span class="p">(</span><span class="n">row</span><span class="p">))</span>
<span class="nb">print</span><span class="p">()</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>XXXX.XXX..X..X..XX..XXX..
X....X..X.X..X.X..X.X..X.
XXX..X..X.X..X.X..X.X..X.
X....XXX..X..X.XXXX.XXX..
X....X....X..X.X..X.X.X..
X....X.....XX..X..X.X..X.

CPU times: user 3.25 ms, sys: 1.43 ms, total: 4.69 ms
Wall time: 3.42 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-9:-Sensor-Boost">Day 9: Sensor Boost<a class="anchor-link" href="#Day-9:-Sensor-Boost">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[29]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="c1"># GET LEVEL INPUT</span>
<span class="n">boost_prog_raw</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;09&quot;</span><span class="p">)</span>
<span class="n">boost_prog_list</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">boost_prog_raw</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)))</span>
<span class="n">boost_prog</span> <span class="o">=</span> <span class="nb">tuple</span><span class="p">(</span><span class="n">boost_prog_list</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[30]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">BOOST_INPUT</span> <span class="o">=</span> <span class="mi">1</span>

<span class="n">_</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="n">boost_prog</span><span class="p">)</span><span class="o">+</span><span class="p">[</span><span class="mi">0</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">9999</span><span class="p">)],</span> <span class="p">[</span><span class="n">BOOST_INPUT</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 2204990589&#39;

&#39;TIME............................................................&#39;
CPU times: user 1.58 ms, sys: 131 µs, total: 1.71 ms
Wall time: 1.71 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[31]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">SENSOR_MODE</span> <span class="o">=</span> <span class="mi">2</span>

<span class="n">_</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="n">boost_prog</span><span class="p">)</span><span class="o">+</span><span class="p">[</span><span class="mi">0</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">9999</span><span class="p">)],</span> <span class="p">[</span><span class="n">SENSOR_MODE</span><span class="p">])</span>
<span class="n">print_result</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">])</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 50008&#39;

&#39;TIME............................................................&#39;
CPU times: user 1.18 s, sys: 8.55 ms, total: 1.19 s
Wall time: 1.2 s
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-10:-Monitoring-Station">Day 10: Monitoring Station<a class="anchor-link" href="#Day-10:-Monitoring-Station">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[32]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">asteroids</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;10&quot;</span><span class="p">)</span><span class="o">.</span><span class="n">splitlines</span><span class="p">()</span>
<span class="n">asteroid_grid</span> <span class="o">=</span> <span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">([</span><span class="n">np</span><span class="o">.</span><span class="n">array</span><span class="p">(</span><span class="nb">list</span><span class="p">(</span><span class="n">belt</span><span class="p">))</span> <span class="k">for</span> <span class="n">belt</span> <span class="ow">in</span> <span class="n">asteroids</span><span class="p">])</span>
<span class="n">asteroid_set</span> <span class="o">=</span> <span class="nb">frozenset</span><span class="p">(</span><span class="nb">zip</span><span class="p">(</span><span class="o">*</span><span class="n">np</span><span class="o">.</span><span class="n">where</span><span class="p">(</span><span class="n">asteroid_grid</span> <span class="o">==</span> <span class="s1">&#39;#&#39;</span><span class="p">)[::</span><span class="o">-</span><span class="mi">1</span><span class="p">]))</span>

<span class="n">X</span> <span class="o">=</span> <span class="mi">0</span>
<span class="n">Y</span> <span class="o">=</span> <span class="mi">1</span>

<span class="n">sort_order</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s1">&#39;+&#39;</span><span class="p">:</span> <span class="mi">1</span><span class="p">,</span>
    <span class="s1">&#39;-&#39;</span><span class="p">:</span> <span class="o">-</span><span class="mi">1</span>
<span class="p">}</span>

<span class="k">def</span> <span class="nf">calc_slope</span><span class="p">(</span><span class="n">p1</span><span class="p">,</span> <span class="n">p2</span><span class="p">):</span>
    <span class="k">if</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">):</span>
        <span class="k">return</span> <span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">inf</span><span class="p">,</span> <span class="s1">&#39;+&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">])</span> <span class="o">&lt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;-&#39;</span><span class="p">)</span>
    <span class="k">if</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">==</span><span class="mi">0</span><span class="p">):</span>
        <span class="k">return</span> <span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;-&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;+&#39;</span><span class="p">)</span>
    <span class="k">return</span> <span class="p">((</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">])</span><span class="o">/</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">]),</span> <span class="s1">&#39;-&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;+&#39;</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[33]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>

<span class="n">visible_sets</span> <span class="o">=</span> <span class="p">[(</span><span class="n">asteroid</span><span class="p">,</span> <span class="nb">set</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="n">calc_slope</span><span class="p">,</span> <span class="n">itertools</span><span class="o">.</span><span class="n">repeat</span><span class="p">(</span><span class="n">asteroid</span><span class="p">),</span> <span class="n">asteroid_set</span><span class="o">-</span><span class="p">{</span><span class="n">asteroid</span><span class="p">})))</span> <span class="k">for</span> <span class="n">asteroid</span> <span class="ow">in</span> <span class="n">asteroid_set</span><span class="p">]</span>
  
<span class="n">monitoring_location</span><span class="p">,</span> <span class="n">visible_asteroids</span> <span class="o">=</span> <span class="nb">max</span><span class="p">(</span><span class="n">visible_sets</span><span class="p">,</span> <span class="n">key</span> <span class="o">=</span> <span class="k">lambda</span> <span class="n">x</span><span class="p">:</span> <span class="nb">len</span><span class="p">(</span><span class="n">x</span><span class="p">[</span><span class="mi">1</span><span class="p">]))</span>
<span class="n">print_result</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;</span><span class="si">{</span><span class="nb">len</span><span class="p">(</span><span class="n">visible_asteroids</span><span class="p">)</span><span class="si">}</span><span class="s2"> asteroids visible at </span><span class="si">{</span><span class="n">monitoring_location</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 284 asteroids visible at (20, 19)&#39;

&#39;TIME............................................................&#39;
CPU times: user 299 ms, sys: 5.79 ms, total: 305 ms
Wall time: 307 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-two">part two<a class="anchor-link" href="#part-two">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[34]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">MONITORING_STATION</span> <span class="o">=</span> <span class="p">(</span><span class="mi">20</span><span class="p">,</span> <span class="mi">19</span><span class="p">)</span>
<span class="n">REMAINING_ASTEROIDS</span> <span class="o">=</span> <span class="n">asteroid_set</span><span class="o">-</span><span class="p">{</span><span class="n">MONITORING_STATION</span><span class="p">}</span>

<span class="k">def</span> <span class="nf">l1</span><span class="p">(</span><span class="n">p1</span><span class="p">,</span> <span class="n">p2</span><span class="p">):</span>
    <span class="k">return</span> <span class="nb">abs</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span><span class="o">+</span><span class="nb">abs</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">])</span>

<span class="k">def</span> <span class="nf">calc_slope_and_dist</span><span class="p">(</span><span class="n">p1</span><span class="p">,</span> <span class="n">p2</span><span class="p">):</span>
    <span class="n">dist</span> <span class="o">=</span> <span class="n">l1</span><span class="p">(</span><span class="n">p1</span><span class="p">,</span><span class="n">p2</span><span class="p">)</span>
    <span class="k">if</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">]</span> <span class="o">==</span> <span class="mi">0</span><span class="p">):</span>
        <span class="k">return</span> <span class="p">(</span><span class="n">np</span><span class="o">.</span><span class="n">inf</span><span class="p">,</span> <span class="s1">&#39;+&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;-&#39;</span><span class="p">,</span> <span class="n">dist</span><span class="p">)</span>
    <span class="k">if</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">==</span><span class="mi">0</span><span class="p">):</span>
        <span class="k">return</span> <span class="p">(</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;-&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;+&#39;</span><span class="p">,</span> <span class="n">dist</span><span class="p">)</span>
    <span class="k">return</span> <span class="p">(</span><span class="o">-</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">Y</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">Y</span><span class="p">])</span><span class="o">/</span><span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">]),</span> <span class="s1">&#39;-&#39;</span> <span class="k">if</span> <span class="p">(</span><span class="n">p1</span><span class="p">[</span><span class="n">X</span><span class="p">]</span><span class="o">-</span><span class="n">p2</span><span class="p">[</span><span class="n">X</span><span class="p">])</span> <span class="o">&gt;</span> <span class="mi">0</span> <span class="k">else</span> <span class="s1">&#39;+&#39;</span><span class="p">,</span> <span class="n">dist</span><span class="p">)</span>

<span class="n">visible_list</span> <span class="o">=</span> <span class="p">[(</span><span class="n">asteroid</span><span class="p">,</span> <span class="n">calc_slope_and_dist</span><span class="p">(</span><span class="n">MONITORING_STATION</span><span class="p">,</span> <span class="n">asteroid</span><span class="p">))</span> <span class="k">for</span> <span class="n">asteroid</span> <span class="ow">in</span> <span class="n">REMAINING_ASTEROIDS</span><span class="p">]</span>
<span class="n">visible_list</span><span class="o">.</span><span class="n">sort</span><span class="p">(</span><span class="n">key</span><span class="o">=</span><span class="k">lambda</span> <span class="n">k</span><span class="p">:</span> <span class="p">(</span><span class="n">sort_order</span><span class="p">[</span><span class="n">k</span><span class="p">[</span><span class="mi">1</span><span class="p">][</span><span class="mi">1</span><span class="p">]],</span> <span class="n">k</span><span class="p">[</span><span class="mi">1</span><span class="p">][</span><span class="mi">0</span><span class="p">],</span> <span class="o">-</span><span class="n">k</span><span class="p">[</span><span class="mi">1</span><span class="p">][</span><span class="mi">2</span><span class="p">]),</span> <span class="n">reverse</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>

<span class="n">visible_stacked</span> <span class="o">=</span> <span class="p">[</span><span class="nb">list</span><span class="p">(</span><span class="n">g</span><span class="p">)</span> <span class="k">for</span> <span class="n">k</span><span class="p">,</span> <span class="n">g</span> <span class="ow">in</span> <span class="n">itertools</span><span class="o">.</span><span class="n">groupby</span><span class="p">(</span><span class="n">visible_list</span><span class="p">,</span> <span class="n">key</span><span class="o">=</span><span class="k">lambda</span> <span class="n">k</span><span class="p">:</span> <span class="n">k</span><span class="p">[</span><span class="mi">1</span><span class="p">][:</span><span class="mi">1</span><span class="p">])]</span>
<span class="n">two_hundredth_vape</span> <span class="o">=</span> <span class="n">visible_stacked</span><span class="p">[</span><span class="mi">199</span><span class="p">][</span><span class="mi">0</span><span class="p">][</span><span class="mi">0</span><span class="p">]</span>

<span class="n">output_val</span> <span class="o">=</span> <span class="n">two_hundredth_vape</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="o">*</span><span class="mi">100</span><span class="o">+</span><span class="n">two_hundredth_vape</span><span class="p">[</span><span class="mi">1</span><span class="p">]</span>

<span class="n">print_result</span><span class="p">(</span><span class="n">output_val</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>&#39;RESULT: 404&#39;

&#39;TIME............................................................&#39;
CPU times: user 2.63 ms, sys: 376 µs, total: 3 ms
Wall time: 2.66 ms
</pre>
</div>
</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h2 id="Day-11:-Space-Police">Day 11: Space Police<a class="anchor-link" href="#Day-11:-Space-Police">&#182;</a></h2>
</div>
</div>
</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="setup">setup<a class="anchor-link" href="#setup">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[35]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="n">paint_prog</span> <span class="o">=</span> <span class="n">get_level_input</span><span class="p">(</span><span class="s2">&quot;11&quot;</span><span class="p">)</span>
<span class="n">paint_prog</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">int</span><span class="p">,</span> <span class="n">paint_prog</span><span class="o">.</span><span class="n">split</span><span class="p">(</span><span class="s1">&#39;,&#39;</span><span class="p">)))</span>
<span class="n">paint_prog</span> <span class="o">=</span> <span class="nb">tuple</span><span class="p">(</span><span class="n">paint_prog</span><span class="p">)</span>

<span class="n">BLACK</span> <span class="o">=</span> <span class="mi">0</span>
<span class="n">WHITE</span> <span class="o">=</span> <span class="mi">1</span>
<span class="n">DIRECTIONS</span> <span class="o">=</span> <span class="p">[</span><span class="s1">&#39;^&#39;</span><span class="p">,</span><span class="s1">&#39;&gt;&#39;</span><span class="p">,</span><span class="s1">&#39;v&#39;</span><span class="p">,</span> <span class="s1">&#39;&lt;&#39;</span><span class="p">]</span>
<span class="n">DIR_MOVE</span> <span class="o">=</span> <span class="p">{</span>
    <span class="s1">&#39;^&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="mi">1</span><span class="p">],</span>
    <span class="s1">&#39;&gt;&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">],</span>
    <span class="s1">&#39;v&#39;</span><span class="p">:</span> <span class="p">[</span><span class="mi">0</span><span class="p">,</span> <span class="o">-</span><span class="mi">1</span><span class="p">],</span>
    <span class="s1">&#39;&lt;&#39;</span><span class="p">:</span> <span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">,</span> <span class="mi">0</span><span class="p">]</span>
<span class="p">}</span>

<span class="n">ROTATE</span> <span class="o">=</span> <span class="p">{</span>
    <span class="mi">0</span><span class="p">:</span> <span class="o">-</span><span class="mi">1</span><span class="p">,</span>
    <span class="mi">1</span><span class="p">:</span> <span class="mi">1</span>
<span class="p">}</span>
</pre></div>

    </div>
</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[45]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">robot_position</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;^&#39;</span><span class="p">]</span>
<span class="n">white_set</span> <span class="o">=</span> <span class="nb">set</span><span class="p">()</span>
<span class="n">black_set</span> <span class="o">=</span> <span class="p">{(</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">)}</span>

<span class="k">def</span> <span class="nf">get_color</span><span class="p">(</span><span class="n">rob_pos</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">rob_pos</span> <span class="ow">in</span> <span class="n">white_set</span><span class="p">:</span>
        <span class="k">return</span> <span class="n">WHITE</span>
    <span class="k">return</span> <span class="n">BLACK</span>

<span class="k">def</span> <span class="nf">add_color</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">):</span>
    <span class="n">cur_point</span> <span class="o">=</span> <span class="nb">tuple</span><span class="p">(</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">])</span>
    <span class="n">white_set</span><span class="o">-=</span><span class="p">{</span><span class="n">cur_point</span><span class="p">}</span>
    <span class="n">black_set</span><span class="o">-=</span><span class="p">{</span><span class="n">cur_point</span><span class="p">}</span>
    <span class="k">if</span><span class="p">(</span><span class="n">output</span><span class="o">==</span><span class="n">WHITE</span><span class="p">):</span>
        <span class="n">white_set</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">cur_point</span><span class="p">)</span>
    <span class="k">if</span><span class="p">(</span><span class="n">output</span><span class="o">==</span><span class="n">BLACK</span><span class="p">):</span>
        <span class="n">black_set</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">cur_point</span><span class="p">)</span>
        
<span class="k">def</span> <span class="nf">move_robot</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">):</span>
    <span class="n">direction</span> <span class="o">=</span> <span class="n">robot_position</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">dir_index</span> <span class="o">=</span> <span class="n">DIRECTIONS</span><span class="o">.</span><span class="n">index</span><span class="p">(</span><span class="n">direction</span><span class="p">)</span>
    <span class="n">new_dir</span> <span class="o">=</span> <span class="n">DIRECTIONS</span><span class="p">[(</span><span class="n">dir_index</span><span class="o">+</span><span class="n">ROTATE</span><span class="p">[</span><span class="n">output</span><span class="p">])</span><span class="o">%</span><span class="nb">len</span><span class="p">(</span><span class="n">DIRECTIONS</span><span class="p">)]</span>
    <span class="k">return</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">sum</span><span class="p">,</span> <span class="nb">zip</span><span class="p">(</span><span class="o">*</span><span class="p">[</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">],</span> <span class="n">DIR_MOVE</span><span class="p">[</span><span class="n">new_dir</span><span class="p">]])))</span><span class="o">+</span><span class="p">[</span><span class="n">new_dir</span><span class="p">]</span>
    
<span class="k">def</span> <span class="nf">run_robot</span><span class="p">(</span><span class="n">robot_position</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">):</span>
    <span class="n">paint_prog_ex</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">paint_prog</span><span class="p">)</span><span class="o">+</span><span class="p">[</span><span class="mi">0</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">100000</span><span class="p">)]</span>
    <span class="n">ip</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="k">while</span><span class="p">(</span><span class="kc">True</span><span class="p">):</span>
        <span class="n">current_color</span> <span class="o">=</span> <span class="n">get_color</span><span class="p">(</span><span class="nb">tuple</span><span class="p">(</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">]))</span>
        <span class="n">cur_input</span> <span class="o">=</span> <span class="p">[</span><span class="n">current_color</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10</span><span class="p">)]</span>
        <span class="n">ip</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">paint_prog_ex</span><span class="p">,</span> <span class="n">cur_input</span><span class="p">,</span> <span class="n">ip</span> <span class="o">=</span> <span class="n">ip</span><span class="p">,</span> <span class="n">return_on_output</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">outputs</span> <span class="o">==</span> <span class="p">[]:</span>
            <span class="k">break</span>
        <span class="n">add_color</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">)</span>
        <span class="n">ip</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">paint_prog_ex</span><span class="p">,</span> <span class="n">cur_input</span><span class="p">,</span> <span class="n">ip</span> <span class="o">=</span> <span class="n">ip</span><span class="p">,</span> <span class="n">return_on_output</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">outputs</span> <span class="o">==</span> <span class="p">[]:</span>
            <span class="k">break</span>
        <span class="n">robot_position</span> <span class="o">=</span> <span class="n">move_robot</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">robot_position</span><span class="p">)</span>
    <span class="k">return</span> <span class="nb">len</span><span class="p">(</span><span class="n">white_set</span><span class="p">)</span><span class="o">+</span><span class="nb">len</span><span class="p">(</span><span class="n">black_set</span><span class="p">)</span>

<span class="n">run_robot</span><span class="p">(</span><span class="n">robot_position</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>CPU times: user 378 ms, sys: 2.95 ms, total: 381 ms
Wall time: 382 ms
</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt output_prompt">Out[45]:</div>




<div class="output_text output_subarea output_execute_result">
<pre>2293</pre>
</div>

</div>

</div>
</div>

</div>
<div class="cell border-box-sizing text_cell rendered"><div class="prompt input_prompt">
</div><div class="inner_cell">
<div class="text_cell_render border-box-sizing rendered_html">
<h3 id="part-one">part one<a class="anchor-link" href="#part-one">&#182;</a></h3>
</div>
</div>
</div>
<div class="cell border-box-sizing code_cell rendered">
<div class="input">
<div class="prompt input_prompt">In&nbsp;[47]:</div>
<div class="inner_cell">
    <div class="input_area">
<div class=" highlight hl-ipython3"><pre><span></span><span class="o">%%</span><span class="n">time</span>
<span class="n">robot_position</span> <span class="o">=</span> <span class="p">[</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">,</span> <span class="s1">&#39;^&#39;</span><span class="p">]</span>
<span class="n">white_set</span> <span class="o">=</span> <span class="p">{(</span><span class="mi">0</span><span class="p">,</span><span class="mi">0</span><span class="p">)}</span>
<span class="n">black_set</span> <span class="o">=</span> <span class="nb">set</span><span class="p">()</span>

<span class="k">def</span> <span class="nf">get_color</span><span class="p">(</span><span class="n">rob_pos</span><span class="p">):</span>
    <span class="k">if</span> <span class="n">rob_pos</span> <span class="ow">in</span> <span class="n">white_set</span><span class="p">:</span>
        <span class="k">return</span> <span class="n">WHITE</span>
    <span class="k">return</span> <span class="n">BLACK</span>

<span class="k">def</span> <span class="nf">add_color</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">):</span>
    <span class="n">cur_point</span> <span class="o">=</span> <span class="nb">tuple</span><span class="p">(</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">])</span>
    <span class="n">white_set</span><span class="o">-=</span><span class="p">{</span><span class="n">cur_point</span><span class="p">}</span>
    <span class="n">black_set</span><span class="o">-=</span><span class="p">{</span><span class="n">cur_point</span><span class="p">}</span>
    <span class="k">if</span><span class="p">(</span><span class="n">output</span><span class="o">==</span><span class="n">WHITE</span><span class="p">):</span>
        <span class="n">white_set</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">cur_point</span><span class="p">)</span>
    <span class="k">if</span><span class="p">(</span><span class="n">output</span><span class="o">==</span><span class="n">BLACK</span><span class="p">):</span>
        <span class="n">black_set</span><span class="o">.</span><span class="n">add</span><span class="p">(</span><span class="n">cur_point</span><span class="p">)</span>
        
<span class="k">def</span> <span class="nf">move_robot</span><span class="p">(</span><span class="n">output</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">):</span>
    <span class="n">direction</span> <span class="o">=</span> <span class="n">robot_position</span><span class="p">[</span><span class="o">-</span><span class="mi">1</span><span class="p">]</span>
    <span class="n">dir_index</span> <span class="o">=</span> <span class="n">DIRECTIONS</span><span class="o">.</span><span class="n">index</span><span class="p">(</span><span class="n">direction</span><span class="p">)</span>
    <span class="n">new_dir</span> <span class="o">=</span> <span class="n">DIRECTIONS</span><span class="p">[(</span><span class="n">dir_index</span><span class="o">+</span><span class="n">ROTATE</span><span class="p">[</span><span class="n">output</span><span class="p">])</span><span class="o">%</span><span class="nb">len</span><span class="p">(</span><span class="n">DIRECTIONS</span><span class="p">)]</span>
    <span class="k">return</span> <span class="nb">list</span><span class="p">(</span><span class="nb">map</span><span class="p">(</span><span class="nb">sum</span><span class="p">,</span> <span class="nb">zip</span><span class="p">(</span><span class="o">*</span><span class="p">[</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">],</span> <span class="n">DIR_MOVE</span><span class="p">[</span><span class="n">new_dir</span><span class="p">]])))</span><span class="o">+</span><span class="p">[</span><span class="n">new_dir</span><span class="p">]</span>
    
<span class="k">def</span> <span class="nf">run_robot</span><span class="p">(</span><span class="n">robot_position</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">):</span>
    <span class="n">paint_prog_ex</span> <span class="o">=</span> <span class="nb">list</span><span class="p">(</span><span class="n">paint_prog</span><span class="p">)</span><span class="o">+</span><span class="p">[</span><span class="mi">0</span> <span class="k">for</span> <span class="n">_</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">100000</span><span class="p">)]</span>
    <span class="n">ip</span> <span class="o">=</span> <span class="mi">0</span>
    <span class="k">while</span><span class="p">(</span><span class="kc">True</span><span class="p">):</span>
        <span class="n">current_color</span> <span class="o">=</span> <span class="n">get_color</span><span class="p">(</span><span class="nb">tuple</span><span class="p">(</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">]))</span>
        <span class="nb">print</span><span class="p">(</span><span class="n">current_color</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;white set: </span><span class="si">{</span><span class="n">white_set</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;black set: </span><span class="si">{</span><span class="n">black_set</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="nb">tuple</span><span class="p">(</span><span class="n">robot_position</span><span class="p">[:</span><span class="mi">2</span><span class="p">]))</span>
        <span class="nb">print</span><span class="p">()</span>
        <span class="n">cur_input</span> <span class="o">=</span> <span class="p">[</span><span class="n">current_color</span> <span class="k">for</span> <span class="n">x</span> <span class="ow">in</span> <span class="nb">range</span><span class="p">(</span><span class="mi">10</span><span class="p">)]</span>
        <span class="n">ip</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">paint_prog_ex</span><span class="p">,</span> <span class="n">cur_input</span><span class="p">,</span> <span class="n">ip</span> <span class="o">=</span> <span class="n">ip</span><span class="p">,</span> <span class="n">return_on_output</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">outputs</span> <span class="o">==</span> <span class="p">[]:</span>
            <span class="k">break</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;FULL ROUND&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;input: </span><span class="si">{</span><span class="n">cur_input</span><span class="p">[</span><span class="mi">0</span><span class="p">]</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;paint_stage&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;output: </span><span class="si">{</span><span class="n">outputs</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="n">add_color</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">,</span> <span class="n">robot_position</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;robot pos: </span><span class="si">{</span><span class="n">robot_position</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;white set: </span><span class="si">{</span><span class="n">white_set</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;black set: </span><span class="si">{</span><span class="n">black_set</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="n">ip</span><span class="p">,</span> <span class="n">outputs</span> <span class="o">=</span> <span class="n">intcomp</span><span class="o">.</span><span class="n">run_computer</span><span class="p">(</span><span class="n">paint_prog_ex</span><span class="p">,</span> <span class="n">cur_input</span><span class="p">,</span> <span class="n">ip</span> <span class="o">=</span> <span class="n">ip</span><span class="p">,</span> <span class="n">return_on_output</span><span class="o">=</span><span class="kc">True</span><span class="p">)</span>
        <span class="k">if</span> <span class="n">outputs</span> <span class="o">==</span> <span class="p">[]:</span>
            <span class="k">break</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;move_stage&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;output: </span><span class="si">{</span><span class="n">outputs</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="n">robot_position</span> <span class="o">=</span> <span class="n">move_robot</span><span class="p">(</span><span class="n">outputs</span><span class="p">[</span><span class="mi">0</span><span class="p">],</span> <span class="n">robot_position</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">(</span><span class="sa">f</span><span class="s2">&quot;robot pos: </span><span class="si">{</span><span class="n">robot_position</span><span class="si">}</span><span class="s2">&quot;</span><span class="p">)</span>
        <span class="nb">print</span><span class="p">()</span>
    <span class="k">return</span> <span class="nb">len</span><span class="p">(</span><span class="n">white_set</span><span class="p">)</span><span class="o">+</span><span class="nb">len</span><span class="p">(</span><span class="n">black_set</span><span class="p">)</span>

<span class="n">run_robot</span><span class="p">(</span><span class="n">robot_position</span><span class="p">,</span> <span class="n">white_set</span><span class="p">,</span> <span class="n">black_set</span><span class="p">)</span>
</pre></div>

    </div>
</div>
</div>

<div class="output_wrapper">
<div class="output">


<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_stream output_stdout output_text">
<pre>1
white set: {(0, 0)}
black set: set()
(0, 0)

FULL ROUND
input: 1
paint_stage
output: [0]
robot pos: [0, 0, &#39;^&#39;]
white set: set()
black set: {(0, 0)}
move_stage
output: [1]
robot pos: [1, 0, &#39;&gt;&#39;]

0
white set: set()
black set: {(0, 0)}
(1, 0)

FULL ROUND
input: 0
paint_stage
output: [0]
robot pos: [1, 0, &#39;&gt;&#39;]
white set: set()
black set: {(1, 0), (0, 0)}
move_stage
output: [1]
robot pos: [1, -1, &#39;v&#39;]

0
white set: set()
black set: {(1, 0), (0, 0)}
(1, -1)

</pre>
</div>
</div>

<div class="output_area">

    <div class="prompt"></div>


<div class="output_subarea output_text output_error">
<pre>
<span class="ansi-red-fg">---------------------------------------------------------------------------</span>
<span class="ansi-red-fg">KeyError</span>                                  Traceback (most recent call last)
<span class="ansi-green-fg">&lt;timed exec&gt;</span> in <span class="ansi-cyan-fg">&lt;module&gt;</span>

<span class="ansi-green-fg">&lt;timed exec&gt;</span> in <span class="ansi-cyan-fg">run_robot</span><span class="ansi-blue-fg">(robot_position, white_set, black_set)</span>

<span class="ansi-green-fg">~/Desktop/hobbies/code/jupyter-notebooks/advent_2019/intcomp.py</span> in <span class="ansi-cyan-fg">run_computer</span><span class="ansi-blue-fg">(comp_string, c_i, ip, rel_base, print_output, return_on_output)</span>
<span class="ansi-green-intense-fg ansi-bold">    107</span>         input_modes <span class="ansi-blue-fg">=</span> <span class="ansi-blue-fg">[</span>int<span class="ansi-blue-fg">(</span>opcode_and_settings<span class="ansi-blue-fg">[</span><span class="ansi-blue-fg">-</span><span class="ansi-cyan-fg">3</span><span class="ansi-blue-fg">]</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">,</span> int<span class="ansi-blue-fg">(</span>opcode_and_settings<span class="ansi-blue-fg">[</span><span class="ansi-blue-fg">-</span><span class="ansi-cyan-fg">4</span><span class="ansi-blue-fg">]</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">,</span> int<span class="ansi-blue-fg">(</span>opcode_and_settings<span class="ansi-blue-fg">[</span><span class="ansi-blue-fg">-</span><span class="ansi-cyan-fg">5</span><span class="ansi-blue-fg">]</span><span class="ansi-blue-fg">)</span><span class="ansi-blue-fg">]</span>
<span class="ansi-green-intense-fg ansi-bold">    108</span> 
<span class="ansi-green-fg">--&gt; 109</span><span class="ansi-red-fg">         </span>window_size <span class="ansi-blue-fg">=</span> operation_length<span class="ansi-blue-fg">[</span>opcode<span class="ansi-blue-fg">]</span>
<span class="ansi-green-intense-fg ansi-bold">    110</span>         win <span class="ansi-blue-fg">=</span> comp_string<span class="ansi-blue-fg">[</span>ip<span class="ansi-blue-fg">:</span> ip<span class="ansi-blue-fg">+</span>window_size<span class="ansi-blue-fg">]</span>
<span class="ansi-green-intense-fg ansi-bold">    111</span>         ip <span class="ansi-blue-fg">+=</span> window_size

<span class="ansi-red-fg">KeyError</span>: 36</pre>
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
 

