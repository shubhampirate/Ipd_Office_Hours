import React, { useState } from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Paper from "@mui/material/Paper";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import { useNavigate } from "react-router-dom";
import { useTheme } from "@mui/material";
import { tokens } from "../../theme";
import logo from "../../assets/logo.png";
import baseUrl from "../../baseUrl";
//import cover from "../../assets/images/cover.png";

export default function Login() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

    const theme = useTheme();
    const colors = tokens(theme.palette.mode);
    const navigate = useNavigate();

	var myHeaders = new Headers();
	myHeaders.append(
		"Cookie",
		"csrftoken=fQ5GcS3afHVVVyREFENw1Ub54RZgwlMkIFicrHrxOrddyB7xgNi46AaN5B6A4090; sessionid=vkfter6wndyr2xly3808yhu1meqwl3gn"
	);

	const handleSubmit = (event) => {
		event.preventDefault();
		var formdata = new FormData();
		formdata.append("email", email);
		formdata.append("password", password);
		fetch(baseUrl + "login/", {
			method: "POST",
			headers: myHeaders,
			body: formdata,
			redirect: "follow",
		})
			.then((response) => response.json())
			.then((result) => {
				if(result.token){
					console.log(result.token)
					navigate('/')
                    localStorage.setItem('token', result.token)
				}else{
					alert('Invalid credentials')
				}
				// result.token ? navigate("/booking"):
				// alert("invalid"), navigate("/signup")
			})
			.catch((error) => {
				console.log(error)
				alert('Invalid Credentials')
			});
		// eslint-disable-next-line no-console
	};

	return (
		<Grid
			container
			component="main"
            justifyContent="center"
            display="flex"
            alignItems="center"
			//sx={{ height: "100vh", overflow: "hidden" }}
		>
			<Grid
				item
				xs={12}
				sm={6}
				md={6}
				component={Paper}
				elevation={6}
				square
				backgroundColor= {colors.primary[400]} //"#ececed"
			>
				<div>
					<Box
						sx={{
							my: 8,
							mx: 4,
							display: "flex",
							flexDirection: "column",
							alignItems: "center",
						}}
                        py={5}
					>
                        <img src={logo} alt="logo" height={100} />
						<Typography
							//component="h1"
							//variant="h5"
							//display="flex"
							//flexDirection="column"
							//alignItems="right"
							//sx={{ mt: 8, fontWeight: "bold" }}
                            variant="h2"
                            color={colors.grey[100]}
                            fontWeight="bold"
                            sx={{ m: "0 0 5px 0" }}
						>
							SIGN IN
						</Typography>
						<Box
							component="form"
							noValidate
							onSubmit={handleSubmit}
							sx={{ mt: 1 }}
						>
							<TextField
								margin="normal"
								required
								sx={{ width: "350px" }}
								id="email"
								label="Email"
								name="email"
								autoComplete="email"
								autoFocus
                                variant="filled"
								onChange={(e) => setEmail(e.target.value)}
							/>
							<TextField
								margin="normal"
								required
								sx={{
									width: "350px",
									display: "flex",
									flexDirection: "column",
								}}
								name="password"
								label="Password"
								type="password"
								id="password"
								autoComplete="current-password"
                                variant="filled"
								onChange={(e) => setPassword(e.target.value)}
							/>
							{/* <p style={{ textAlign: 'center', fontSize: '0.89rem', color: '#1F2128' }}>Don't have an account? <span onClick={() => navigate('/signup')} style={{ cursor: 'pointer', color: 'blue' }}>Sign Up</span></p> */}
							<Typography variant="h5" color={colors.greenAccent[400]} style={{ textAlign: 'center', fontSize: '0.89rem', marginBottom: '15px', marginTop: '20px' }} >
                                Forgot Credentials? Contact Admin.
                            </Typography>
                            <Button
								//className="main_btn"
								type="submit"
								fullWidth
								// variant="outlined"
                                color="secondary" 
                                variant="contained"
							>
								Sign In
							</Button>
						</Box>
					</Box>
				</div>
			</Grid>

			{/* <Grid
				item
				xs={false}
				sm={4}
				md={4}
				 sx={{
				 	backgroundImage: login,
				 	backgroundSize: "cover",
				 	backgroundPosition: "center",
				 	backgroundColor: "#1F2128",
				 }}
			>
				{ <img
					src={cover}
					style={{ width: "100%", height: "100vh" }}
					alt="login-img"
				/> }
				<Button
					className="login_button"
					type="button"
					variant="contained"
					onClick={() => {
						navigate("/login");
					}}
					sx={{
						mt: -145,
						mb: 2,
						mr: 58,
						padding: "10px",
						width: "110px",
						backgroundColor: "#ECECED",
						paddingRight: "25px",
						paddingTop: "10px",
						paddingBottom: "10px",
						color: "#1F2128",
						fontWeight: "bold",
						borderRadius: '0px 25px 25px 0px !important'
					}}
				>
					Login
				</Button>
				<Button
					className="login_button"
					type="button"
					variant="contained"
					onClick={() => {
						navigate("/signup");
					}}
					sx={{
						mt: -135,
						mb: 2,
						mr: 58,
						padding: "10px",
						width: "110px",
						backgroundColor: "#1F2128",
						paddingRight: "25px",
						paddingTop: "10px",
						paddingBottom: "10px",
						color: "#ECECED",
						fontWeight: "bold",
						borderRadius: '0px 25px 25px 0px !important',
					}}
				 sx={{ "&:hover": { backgroundColor:"white"} }}
				>
					Sign Up
				</Button>
				<Typography
					component="h6"
					variant="h2"
					fontWeight="bold"
					fontSize="35px"
					color="white"
					sx={{
						mt: -55,
						mr: 12,
						ml: 15,
						opacity: 1,
					}}
				>
					Welcome, Back
				</Typography>
                </Grid> */}
		</Grid>
	);
}