from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,\
 TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, EqualTo, Optional


class RegisterForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         Length(min=3, max=15)])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=3, max=15)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Add_RecipeForm(FlaskForm):
    recipe_name = StringField('Recipe Name',
                              validators=[DataRequired()])
    recipe_description = TextAreaField('Recipe Description',
                                       validators=[DataRequired()])
    cooking_time = IntegerField('Cooking Time (minutes)',
                                validators=[DataRequired()])
    servings = IntegerField('Number of Servings', validators=[DataRequired()])
    image = StringField('Recipe Image', validators=[Optional()])
    ingredients = TextAreaField('Ingredients',
                                validators=[DataRequired()])
    recipe_directions = TextAreaField('Directions',
                                      validators=[DataRequired()])
    submit = SubmitField('Add Recipe')
