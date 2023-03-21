import { Box, Grid, Paper, Typography, useTheme } from '@mui/material';
import { tokens } from "../../theme";
import profilePic from "../../assets/logo.png";

const ProfilePage = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);

  const name = 'John Doe';
  const role = 'Software Developer';
  const email = 'johndoe@example.com';
  const efficiency = [60, 80, 90, 75, 85, 70, 95];

  return (
    <>

        <Grid
			container
			component="main"
            display="flex"
            alignItems="center"
            justifyContent="center"
			//sx={{ height: "100vh", overflow: "hidden" }}
		>
			<Grid
				item
				xs={12}
				sm={5}
				md={5}
				component={Paper}
				elevation={6}
				square
				backgroundColor= {colors.primary[400]}
                mx={2}
                justifyContent="center"
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
                        py={2}
					>
                        <img src={profilePic} alt="logo" height={200} width={200}/>
						<Typography
                            variant="h3"
                            color={colors.grey[100]}
                            fontWeight="bold"
                            sx={{ m: "0 0 5px 0" }}
						>
							{name}
						</Typography>
                        <Typography
                            variant="h5"
                            color={colors.grey[100]}
                            fontWeight="bold"
                            sx={{ m: "0 0 5px 0" }}
                        >
                            {role}
                        </Typography>
                        <Typography
                            variant="h6"
                            color={colors.grey[100]}
                            fontWeight="bold"
                            sx={{ m: "0 0 5px 0" }}
                        >
                            {email}
                        </Typography>
                        </Box>
				</div>
			</Grid>
            </Grid>
    </>
  );
};

export default ProfilePage;