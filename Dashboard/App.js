import React from 'react'
import './slider.less'
import Graph from './Components/Graph'
import Graph2 from './Components/Graph2'
import {RangeSlider} from 'rsuite'


export default function App() {
	const [data, setData] = React.useState();
	const [loading, setLoading] = React.useState(true);
	const [season , setSeason] = React.useState([1982, 2021]);
	const [leagueStatus, setLeagueStatus] = React.useState({NL:true, AL:true});

	const rawData = async () => {
		try {
			const response = await fetch('http://localhost:5000/*');
			const jsonData = await response.json();
			setData(jsonData);
			setLoading(false);
		} catch (err) {
			console.error(err.message);
		}
	}

	function Seasonator(event) {setSeason(event)};
	function leagueClicked (event) {
		const {name, value, type, checked} = event.target;
		setLeagueStatus(prevLeague => ({...prevLeague, [name]: type==='checkbox' ? checked : value}));
	};

	React.useEffect(() => {
		rawData();
	}, []);

	return (
		<div className="App">
			{!loading && 
			<>
				<div className='title'><h1>BaseBool Dashboard</h1></div>
				<div className='silder-component'>
					<h1> Filter By Season:  </h1>
					<div className='slider'>
						<RangeSlider 
							min={1982} 
							max={2021} 
							defaultValue={[1997, 2021]} 
							onChange={Seasonator}
						/>
					</div>
					<fieldset>
						<legend>Filter by League </legend>
						<input 
							type="checkbox"
							id="NL"
							name='NL'
							value="NL"
							onChange={leagueClicked}
							checked={leagueStatus.NL === true}
						/>
						<label htmlFor="NL">National</label>
						<br />
						<input 
							type="checkbox"
							id="AL"
							name='AL'
							value="AL"
							onChange={leagueClicked}
							checked={leagueStatus.AL === true}

						/>
						<label htmlFor="AL">American</label>
					</fieldset>

				</div>
			</>}
			<Graph2
				data = {data}
				loading = {loading}
				season = {season}
				leagueStatus = {leagueStatus}
			/>
			<Graph
				data = {data}
				season = {season}
				leagueStatus = {leagueStatus}
			/>

		</div>
	);
}
