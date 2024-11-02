# Django Model Logger

A simple and flexible Django app for logging model actions and changes. This package allows developers to easily add logging capabilities to their Django models using decorators.

## Features

- 🚀 Easy to integrate with existing Django projects
- 🎯 Generic relations to work with any model
- 📝 Customizable log names and descriptions
- ⏰ Automatic timestamp tracking
- 🔍 Simple log retrieval
- 🎨 Clean and intuitive API

## Installation

1. Install using pip:

2. Add 'model_logger' to your INSTALLED_APPS in settings.py:

3. Run migrations:

## Usage

### Basic Usage

### Retrieving Logs

```python
from django.contrib.contenttypes.models import ContentType
from model_logger.models import ModelLog

# Get all logs for a specific article
article = Article.objects.get(id=1)
logs = ModelLog.objects.filter(
    content_type=ContentType.objects.get_for_model(Article),
    object_id=article.id
)

# Get all logs across all models
all_logs = ModelLog.objects.all()
```

### ModelLog Fields

The `ModelLog` model includes the following fields:

- `name`: The name of the logged action
- `description`: Detailed description of the action
- `timestamp`: When the action occurred
- `content_type`: The model type being logged
- `object_id`: The specific object's ID
- `content_object`: Generic foreign key to the logged object

## Advanced Usage

### Custom Log Names and Descriptions

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    
    @log_action(
        name="Article Published",
        description="Article was published to the main page"
    )
    def publish(self):
        self.is_published = True
        self.save()
```

### Dynamic Descriptions

```python
class Article(models.Model):
    title = models.CharField(max_length=100)
    
    @log_action(
        name="Title Change",
        description="Title changed from '{old_title}' to '{new_title}'"
    )
    def update_title(self, new_title):
        old_title = self.title
        self.title = new_title
        self.save()
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Requirements

- Python 3.6+
- Django 3.2+

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

If you encounter any problems or have suggestions, please [open an issue](https://github.com/hasan-furkan/django-model-logger/issues) on GitHub.

## Authors

- Hasan Furkan - Initial work - [YourGitHubUsername](https://github.com/hasan-furkan)

## Acknowledgments

- Thanks to the Django community for inspiration
- All the contributors who participate in this project
```

Remember to replace the following placeholders:
- `License` in the LICENSE file
- `yourusername` in the README.md file
- Update the year in the LICENSE if needed
- Add your actual GitHub username and links

The README.md provides:
1. Clear installation instructions
2. Usage examples
3. Advanced usage scenarios
4. Contributing guidelines
5. License information
6. Support information

You might want to add:
1. Screenshots or GIFs demonstrating usage
2. More detailed examples
3. Troubleshooting section
4. Changelog
5. FAQ section

as your package grows and users provide feedback.

