import doctest
import publicsuffix
import unittest
import sys
import warnings

if sys.version < '3':
	import codecs
	def u(x):
		return codecs.unicode_escape_decode(x)[0]
else:
	def u(x):
		return x

class TestPublicSuffix(unittest.TestCase):
	def test_empty(self):
		psl = publicsuffix.PublicSuffixList([])

		self.assertEqual(psl.get_public_suffix("com"), "com")
		self.assertEqual(psl.get_public_suffix("COM"), "com")
		self.assertEqual(psl.get_public_suffix(".com"), "com")
		self.assertEqual(psl.get_public_suffix("a.example.com"), "com")

	def test_basic(self):
		psl = publicsuffix.PublicSuffixList([
			"com"])

		self.assertEqual(psl.get_public_suffix("a.example.com"), "example.com")
		self.assertEqual(psl.get_public_suffix("a.a.example.com"), "example.com")
		self.assertEqual(psl.get_public_suffix("a.a.a.example.com"), "example.com")
		self.assertEqual(psl.get_public_suffix("A.example.com"), "example.com")
		self.assertEqual(psl.get_public_suffix(".a.a.example.com"), "example.com")

	def test_exception(self):
		psl = publicsuffix.PublicSuffixList([
			"*.example.com",
			"!b.example.com"])

		self.assertEqual(psl.get_public_suffix("a.example.com"), "a.example.com")
		self.assertEqual(psl.get_public_suffix("a.a.example.com"), "a.a.example.com")
		self.assertEqual(psl.get_public_suffix("a.a.a.example.com"), "a.a.example.com")
		self.assertEqual(psl.get_public_suffix("a.a.a.a.example.com"), "a.a.example.com")

		self.assertEqual(psl.get_public_suffix("b.example.com"), "b.example.com")
		self.assertEqual(psl.get_public_suffix("b.b.example.com"), "b.example.com")
		self.assertEqual(psl.get_public_suffix("b.b.b.example.com"), "b.example.com")
		self.assertEqual(psl.get_public_suffix("b.b.b.b.example.com"), "b.example.com")

	def test_fqdn(self):
		psl = publicsuffix.PublicSuffixList([
			"com"])

		self.assertEqual(psl.get_public_suffix("example.com."), "example.com")

	def test_unicode(self):
		psl = publicsuffix.PublicSuffixList([
			u("\u0440\u0444")])

		self.assertEqual(psl.get_public_suffix(u("\u0440\u0444")), u("\u0440\u0444"))
		self.assertEqual(psl.get_public_suffix(u("example.\u0440\u0444")), u("example.\u0440\u0444"))
		self.assertEqual(psl.get_public_suffix(u("a.example.\u0440\u0444")), u("example.\u0440\u0444"))
		self.assertEqual(psl.get_public_suffix(u("a.a.example.\u0440\u0444")), u("example.\u0440\u0444"))

	def _get_builtin_psl(self):

		with warnings.catch_warnings(record=True) as w:
			warnings.simplefilter("always")
			psl = publicsuffix.PublicSuffixList()

		self.assertEqual(len(w), 1)
		self.assertTrue(issubclass(w[0].category, DeprecationWarning))
		self.assertTrue("deprecated" in str(w[0].message))

		return psl

	def test_publicsuffix_org_list_test(self):

		psl = self._get_builtin_psl()

		def checkPublicSuffix(a, b):
			self.assertEqual(psl.get_public_suffix(a), b)

		# Mixed case.
		checkPublicSuffix('COM', 'com');
		checkPublicSuffix('example.COM', 'example.com');
		checkPublicSuffix('WwW.example.COM', 'example.com');
		# Leading dot.
		checkPublicSuffix('.com', 'com');
		checkPublicSuffix('.example', 'example');
		checkPublicSuffix('.example.com', 'example.com');
		checkPublicSuffix('.example.example', 'example');
		# Unlisted TLD.
		checkPublicSuffix('example', 'example');
		checkPublicSuffix('example.example', 'example');
		checkPublicSuffix('b.example.example', 'example');
		checkPublicSuffix('a.b.example.example', 'example');
		# Listed, but non-Internet, TLD.
		checkPublicSuffix('local', 'local');
		checkPublicSuffix('example.local', 'local');
		checkPublicSuffix('b.example.local', 'local');
		checkPublicSuffix('a.b.example.local', 'local');
		# TLD with only 1 rule.
		checkPublicSuffix('biz', 'biz');
		checkPublicSuffix('domain.biz', 'domain.biz');
		checkPublicSuffix('b.domain.biz', 'domain.biz');
		checkPublicSuffix('a.b.domain.biz', 'domain.biz');
		# TLD with some 2-level rules.
		checkPublicSuffix('com', 'com');
		checkPublicSuffix('example.com', 'example.com');
		checkPublicSuffix('b.example.com', 'example.com');
		checkPublicSuffix('a.b.example.com', 'example.com');
		checkPublicSuffix('uk.com', 'uk.com');
		checkPublicSuffix('example.uk.com', 'example.uk.com');
		checkPublicSuffix('b.example.uk.com', 'example.uk.com');
		checkPublicSuffix('a.b.example.uk.com', 'example.uk.com');
		checkPublicSuffix('test.ac', 'test.ac');
		# TLD with only 1 (wildcard) rule.
		checkPublicSuffix('bd', 'bd');
		checkPublicSuffix('c.bd', 'c.bd');
		checkPublicSuffix('b.c.bd', 'b.c.bd');
		checkPublicSuffix('a.b.c.bd', 'b.c.bd');
		# More complex TLD.
		checkPublicSuffix('jp', 'jp');
		checkPublicSuffix('test.jp', 'test.jp');
		checkPublicSuffix('www.test.jp', 'test.jp');
		checkPublicSuffix('ac.jp', 'ac.jp');
		checkPublicSuffix('test.ac.jp', 'test.ac.jp');
		checkPublicSuffix('www.test.ac.jp', 'test.ac.jp');
		checkPublicSuffix('kobe.jp', 'kobe.jp');
		checkPublicSuffix('c.kobe.jp', 'c.kobe.jp');
		checkPublicSuffix('b.c.kobe.jp', 'b.c.kobe.jp');
		checkPublicSuffix('a.b.c.kobe.jp', 'b.c.kobe.jp');
		checkPublicSuffix('city.kobe.jp', 'city.kobe.jp');	# Exception rule.
		checkPublicSuffix('www.city.kobe.jp', 'city.kobe.jp');	# Exception rule.
		# US K12.
		checkPublicSuffix('us', 'us');
		checkPublicSuffix('test.us', 'test.us');
		checkPublicSuffix('www.test.us', 'test.us');
		checkPublicSuffix('ak.us', 'ak.us');
		checkPublicSuffix('test.ak.us', 'test.ak.us');
		checkPublicSuffix('www.test.ak.us', 'test.ak.us');
		checkPublicSuffix('k12.ak.us', 'k12.ak.us');
		checkPublicSuffix('test.k12.ak.us', 'test.k12.ak.us');
		checkPublicSuffix('www.test.k12.ak.us', 'test.k12.ak.us');

	def test_publicsuffix_org_list_unicode(self):

		psl = self._get_builtin_psl()

		def checkPublicSuffix(a, b):
			self.assertEqual(psl.get_public_suffix(a), b)

		checkPublicSuffix(u('www.\u9999\u6e2f'), u('www.\u9999\u6e2f'))

	def test_fetch(self):
		f = publicsuffix.fetch()
		psl = publicsuffix.PublicSuffixList(f)

		self.assertEqual(psl.get_public_suffix("www.example.com"), "example.com")
		self.assertEqual(psl.get_public_suffix(u('www.\u9999\u6e2f')), u('www.\u9999\u6e2f'))

def additional_tests():
	return doctest.DocFileSuite("README.rst")

if __name__ == '__main__':
	unittest.main('tests')
