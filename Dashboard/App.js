import React from 'react'
import './slider.less'
import Xbh from './Components/Xbh'
import Graph from './Components/Graph'
import Graph2 from './Components/Graph2'
import {RangeSlider} from 'rsuite'


export default function App() {
	const [data, setData] = React.useState();
	const [form, setForm] = React.useState({season:[2004,2021],
					mvpAL:'mvp1',mvpNL:'mvp2',NL:true,
						AL:true,MVP:true,nonMVP:true});
	const rawData = async () => {
		try {
			const allResponse = await fetch('http://localhost:5000/');
			const allJsonData = await allResponse.json();
			setData(allJsonData);
		} catch (err) {
			console.error(err.message);
		}
	}

	function formClicked (event) {
		if (event.target !== undefined) {
			setForm(prevForm => ({...prevForm, [event.target.name]: event.target.checked}))
		} else {setForm(prevForm => ({...prevForm, season: event}))}
	};

	React.useEffect(() => {
		rawData();
	}, []);
	React.useEffect(() => {
		data && setForm(prevForm => ({...prevForm,
			mvpAL:data.filter((player) => (player.lgID === 'AL' && 
				player.MVP === '1' && player.Season === '2022'))[0],
			mvpNL:data.filter((player) => (player.lgID === 'NL' && 
				player.MVP === '1' && player.Season === '2022'))[0]
		}));
	}, [data]);

	return (
		<div className="App">
			{data && 
			<>
				<div className='title'><h1>Major League Baseball</h1></div>
				<div className='dashboard-description'>
					<h4>This dashboard shows seasons batting stats from 1982-2021.</h4><h4>They were 
					used to predict 2022's winners with a Logistic Regression.</h4>
				</div>
				<div className='mvp-winners'>
					<div><h3><strong>2022 National League MVP:</strong>  {form.mvpNL.Name}</h3></div>
					<div><h3><strong>2022 American League MVP:</strong>  {form.mvpAL.Name}</h3></div>
				</div>
				<div className='silder-component'>
					<h2> Filter By Season:  </h2>
					<div className='slider'>
						<RangeSlider 
							min={1982} 
							max={2022}
							id="season"
							name='season'
							defaultValue={[2004, 2021]} 
							onChange={formClicked}
						/>
					</div>
					<fieldset>
						<legend> League </legend>
						<input 
							type="checkbox"
							id="NL"
							name='NL'
							value="NL"
							onChange={formClicked}
							checked={form.NL === true}
						/>
						<label htmlFor="NL">National</label>
						<br />
						<input 
							type="checkbox"
							id="AL"
							name='AL'
							value="AL"
							onChange={formClicked}
							checked={form.AL === true}

						/>
						<label htmlFor="AL">American</label>
					</fieldset>
					<fieldset>
						<legend> Player Type </legend>
						<input 
							type="checkbox"
							id="MVP"
							name='MVP'
							value="MVP"
							onChange={formClicked}
							checked={form.MVP === true}
						/>
						<label htmlFor="MVP">MVP</label>
						<br />
						<input 
							type="checkbox"
							id="nonMVP"
							name='nonMVP'
							value="nonMVP"
							onChange={formClicked}
							checked={form.nonMVP === true}

						/>
						<label htmlFor="nonMVP">nonMVP</label>
					</fieldset>
				</div>
			</>}
			<Graph
				data = {data}
				form = {form}
			/>
			<Graph2
				data = {data}
				form = {form}
			/>
			<Xbh 
				data = {data}
				form = {form}
			/>
		</div>
	);
}
